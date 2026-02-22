from duckduckgo_search import DDGS

class SearchTool:
    """
    Provides internet search capabilities for the agent using DuckDuckGo.
    """
    def __init__(self, max_results: int = 3):
        # Limit the number of results to save token space in the LLM context
        self.max_results = max_results

    def search(self, query: str) -> str:
        """
        Searches the web for the given query and returns a formatted summary of the top results.
        """
        try:
            # Initialize the DuckDuckGo search client
            with DDGS() as ddgs:
                # Perform the search and get a limited number of results
                results = list(ddgs.text(query, max_results=self.max_results))

            # Handle the case where the search engine returns nothing
            if not results:
                return f"No results found for query: '{query}'."

            # Format the results into a readable string for the LLM
            formatted_results = []
            for i, res in enumerate(results, 1):
                title = res.get('title', 'No Title')
                body = res.get('body', 'No Description')
                link = res.get('href', 'No Link')

                # Build a structured block for each search result
                result_block = f"Result {i}:\nTitle: {title}\nSummary: {body}\nLink: {link}\n"
                formatted_results.append(result_block)

            # Join all formatted blocks with a separator line
            return "\n---\n".join(formatted_results)

        except Exception as e:
            return f"Error performing search: {str(e)}"