from enum import Enum
from typing import Iterable, Set, Dict, Any, List
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

from rich.progress import track


class ProcessingMode(str, Enum):
    """Defines the available processing modes for URL parameters."""
    REPLACE = "replace"
    APPEND = "append"


def is_valid_url(url: str) -> bool:
    """Checks if a string is a well-formed URL with a scheme and netloc."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except (ValueError, AttributeError):
        return False


def get_deduplication_key(parsed_url, ignore_path: bool) -> str:
    """
    Generates a unique key for a URL to identify duplicates.
    The key is based on the domain, sorted parameter names, and optionally the path.
    """
    query_params = parse_qs(parsed_url.query, keep_blank_values=True)
    sorted_param_names = "&".join(sorted(query_params.keys()))

    if ignore_path:
        return f"{parsed_url.netloc}?{sorted_param_names}"

    return f"{parsed_url.netloc}{parsed_url.path}?{sorted_param_names}"


def process_urls(urls_iterable: Iterable[str], config: dict) -> Dict[str, Any]:
    """
    Processes, modifies, and deduplicates an iterable of URLs based on configuration.
    
    This function processes URLs as a stream to be memory-efficient.
    Returns a dictionary containing the list of refined URLs and processing stats.
    """
    refined_urls: List[str] = []
    seen_keys: Set[str] = set()
    total_input = 0
    
    mode = config.get("mode", ProcessingMode.REPLACE.value)
    value_to_use = config.get("value", "FUZZ")
    exclude_params = set(config.get("exclude_params", []))
    ignore_path = config.get("ignore_path", False)

    # The progress bar will work with iterables, showing progress without a total.
    for url in track(urls_iterable, description="[green]Processing URLs...[/green]"):
        total_input += 1
        if not is_valid_url(url):
            continue

        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query, keep_blank_values=True)
        
        dedup_key = get_deduplication_key(parsed_url, ignore_path)
        if dedup_key in seen_keys:
            continue

        modified_params = {}
        for param, values in query_params.items():
            if param in exclude_params:
                modified_params[param] = values
                continue

            if mode == ProcessingMode.REPLACE.value:
                modified_params[param] = value_to_use
            elif mode == ProcessingMode.APPEND.value:
                modified_params[param] = [v + value_to_use for v in values]

        new_query_string = urlencode(modified_params, doseq=True)
        new_url_parts = parsed_url._replace(query=new_query_string)
        refined_url = urlunparse(new_url_parts)
        
        refined_urls.append(refined_url)
        seen_keys.add(dedup_key)
            
    stats = {
        "total_input": total_input,
        "total_output": len(refined_urls),
        "duplicates_removed": total_input - len(refined_urls)
    }
            
    return {"data": refined_urls, "stats": stats}