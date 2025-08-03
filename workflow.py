# langgraph_tavily_movie_agent.py

from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import TypedDict
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Initialize LLM
llm = ChatGroq(
    model="llama3-8b-8192"
)

# Tavily search tool
tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general"
)

# State schema for LangGraph - Fixed: Added Annotated for proper state handling
class GraphState(TypedDict):
    movie_name: str
    search_results: str
    result: dict
    error: str

# Pydantic model for response class
class MovieInfo(BaseModel):
    poster_url: str = Field(description="First poster URL found, or 'Not available' if none found")
    description: str = Field(description="Short description of the movie")
    imdb_rating: str = Field(description="IMDb rating (e.g., '8.6/10') or 'Not available'")
    watch_link: str = Field(description="Watch link if available, else 'Not available'")

# Output parser
parser = PydanticOutputParser(pydantic_object=MovieInfo)

# Updated prompt template for better structure
prompt_template = PromptTemplate(
    template="""Based on the search results below, extract movie information for '{movie_name}':

Search Results: {search_results}

{format_instructions}

Please provide accurate information based on the search results. If any information is not available, use 'Not available'.
""",
    input_variables=["movie_name", "search_results", "format_instructions"]
)

# Fixed: Separate search and parsing functions
def search_movie_node(state):
    """Search for movie information using Tavily"""
    try:
        movie = state["movie_name"]
        search_query = f"{movie} movie poster IMDb rating watch online"
        
        # Perform search
        search_results = tavily_search_tool.run(search_query)
        
        return {
            "movie_name": movie,
            "search_results": search_results,
            "error": ""
        }
    except Exception as e:
        return {
            "movie_name": state["movie_name"],
            "search_results": "",
            "error": str(e)
        }

def parse_movie_info_node(state):
    """Parse the search results into structured movie information"""
    try:
        if state.get("error"):
            # Return default structure if there was a search error
            return {
                "result": MovieInfo(
                    poster_url="Not available",
                    description="Search failed",
                    imdb_rating="Not available", 
                    watch_link="Not available"
                ).dict()
            }
        
        # Create prompt with search results
        prompt = prompt_template.format(
            movie_name=state["movie_name"],
            search_results=state["search_results"],
            format_instructions=parser.get_format_instructions()
        )
        
        # Use LLM to parse the information
        response = llm.invoke(prompt)
        
        # Extract content from response
        if hasattr(response, 'content'):
            response_text = response.content
        else:
            response_text = str(response)
        
        # Try to parse the response
        try:
            parsed = parser.parse(response_text)
            return {"result": parsed.dict()}
        except Exception as parse_error:
            # Fallback: try to extract JSON from response
            try:
                # Look for JSON in the response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_data = json.loads(json_match.group())
                    # Ensure all required fields are present
                    result = {
                        "poster_url": json_data.get("poster_url", "Not available"),
                        "description": json_data.get("description", "Not available"),
                        "imdb_rating": json_data.get("imdb_rating", "Not available"),
                        "watch_link": json_data.get("watch_link", "Not available")
                    }
                    return {"result": result}
            except:
                pass
            
            # Final fallback
            return {
                "result": {
                    "poster_url": "Not available",
                    "description": f"Could not parse movie information for {state['movie_name']}",
                    "imdb_rating": "Not available",
                    "watch_link": "Not available"
                }
            }
            
    except Exception as e:
        return {
            "result": {
                "poster_url": "Not available", 
                "description": f"Error processing movie information: {str(e)}",
                "imdb_rating": "Not available",
                "watch_link": "Not available"
            }
        }

# LangGraph workflow setup - Fixed: Better error handling and flow
graph_builder = StateGraph(GraphState)

# Add nodes
graph_builder.add_node("search_movie", search_movie_node)
graph_builder.add_node("parse_movie_info", parse_movie_info_node)

# Set entry point and edges
graph_builder.set_entry_point("search_movie")
graph_builder.add_edge("search_movie", "parse_movie_info")
graph_builder.add_edge("parse_movie_info", END)

# Compile the graph
movie_graph = graph_builder.compile()

# Test function
def get_movie_info(movie_name: str):
    """Get structured movie information"""
    try:
        output = movie_graph.invoke({"movie_name": movie_name})
        return output["result"]
    except Exception as e:
        print(f"Error getting movie info: {e}")
        return None

# Run the graph
if __name__ == "__main__":
    # Test with multiple movies
    test_movies = ["Interstellar", "The Matrix", "Inception"]
    
    for movie in test_movies:
        print(f"\n📽️ Movie Info for '{movie}':\n")
        result = get_movie_info(movie)
        if result:
            print(json.dumps(result, indent=2))
        else:
            print("Failed to get movie information")
        print("-" * 50)