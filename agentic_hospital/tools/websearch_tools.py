"""Web search tool using browser-use for real-time information lookup."""

import asyncio
import threading


def web_search(query: str) -> dict:
    """Searches the web for current medical information, drug data, clinical guidelines, and research.

    Use this tool when you need up-to-date information not available in your training data,
    such as latest treatment guidelines, newly approved medications, clinical trial results,
    drug interactions, disease outbreaks, or any current medical literature.

    Args:
        query: The search query string (e.g., 'latest AHA guidelines for heart failure 2024').

    Returns:
        dict: Search results with found information, or error details on failure.
    """
    result: dict = {}

    async def _run_search() -> dict:
        import os
        from browser_use import Agent, Browser                    # noqa: PLC0415
        from browser_use.llm.openrouter.chat import ChatOpenRouter  # noqa: PLC0415

        llm = ChatOpenRouter(
            model="google/gemini-2.5-flash",
            api_key=os.environ.get("OPENROUTER_API_KEY", ""),
        )
        browser = Browser(headless=True)
        agent = Agent(
            task=(
                f"Search the web for: {query}. "
                "Provide a concise, factual summary of the most relevant and up-to-date "
                "information found. Include sources where possible."
            ),
            llm=llm,
            browser=browser,
        )
        history = await agent.run(max_steps=10)
        final = history.final_result()
        if not final:
            extracted = history.extracted_content()
            final = "\n\n".join(extracted) if extracted else "No results found."
        return {
            "status": "success",
            "query": query,
            "result": final,
        }

    def _thread_target() -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result.update(loop.run_until_complete(_run_search()))
        except Exception as exc:
            result.update({
                "status": "error",
                "query": query,
                "message": str(exc),
            })
        finally:
            loop.close()

    thread = threading.Thread(target=_thread_target, daemon=True)
    thread.start()
    thread.join(timeout=120)  # 2-minute hard timeout

    if not result:
        return {
            "status": "timeout",
            "query": query,
            "message": "Web search timed out after 120 seconds.",
        }
    return result
