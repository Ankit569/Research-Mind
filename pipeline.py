from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # search agent working
    print("\n" + "=" * 50)
    print("step 1 - search agent is working ...")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result["messages"][-1].content

    print("\n search result ", state["search_results"])

    # step 2 - reader agent
    print("\n" + "=" * 50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("=" * 50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
    "messages": [
        ("user",
         f"""
Use the scrape_url tool.

From the search results below:

1. Find the most relevant VALID URL
2. Use the scrape_url tool on that URL
3. Extract important insights and detailed information
4. Return clean summarized content

Search Results:
{state['search_results']}
         """)
    ]
})
    state["scraped_content"]= reader_result["messages"][-1].content
    print("\n Scraped Content:\n")
    print(state['scraped_content'])

    # step 3 - writer chain
    print("\n" + "=" * 50)
    print("step 3 - Writer is drafting the report ...")
    print("=" * 50)

    research_combined = (
    f"SEARCH RESULTS:\n{state['search_results'][:1000]}\n\n"
    f"SCRAPED CONTENT:\n{state['scraped_content'][:1000]}"
)
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })

    print("\n Final Report\n", state["report"])
    with open("report.txt", "w", encoding="utf-8") as f:
     f.write(state["report"])

    print("\nReport saved as report.txt")

    # critic report
    print("\n" + "=" * 50)
    print("step 4 - critic is reviewing the report ")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({"report": state["report"]})

    print("\n critic report \n", state["feedback"])
    print("\n" + "=" * 50)
    print("Research Pipeline Completed Successfully ✅")
    print("=" * 50)

    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)
    


