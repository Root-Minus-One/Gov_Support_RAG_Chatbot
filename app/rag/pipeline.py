from app.rag.generation import generate_answer
from app.rag.retrieval import retrieve_chunks
from app.rag.gaurdrails import check_relevance
from app.rag.memory import get_or_create_session, get_history, save_message

from langfuse import observe, propagate_attributes, get_client
from app.schemas import ChatResponse, Citation


@observe
async def run_rag_pipeline(question, session_id_input, category) -> ChatResponse:
        # memory
            session_id = await get_or_create_session(session_id_input)
            history = await get_history(session_id)

            # langfuse trace_id
            client = get_client()
            trace_id = client.get_current_trace_id()
        
            chunks = await retrieve_chunks(question=question, category=category)
        
            is_relevant, message = check_relevance(question=question, reranked_chunks=chunks)

            if not is_relevant:
                await save_message(session_id, "user", question)
                await save_message(session_id, "assistant", message)
                return ChatResponse(success=True,
                                    is_relevant=False,
                                    answer= "Sorry, I don't have information for this question!",
                                    citations=[],
                                    trace_id=trace_id
                                    )
        
            answer = generate_answer(question, chunks, history)
        
            # save messages
            await save_message(session_id, "user", question)
            await save_message(session_id, "assistant", answer)
            
            citations: list[Citation] = [
                    Citation(
                            chunk_id=str(c.get("chunk_id", "NA")),
                            doc_id=str(c.get("doc_id", "NA")),
                            document_title=str(c.get("document_title", "Untitled Document")),
                            category=str(c.get("category", "unknown")),
                            page_number=c.get("page_number"),
                            score=float(c.get("score", c.get("rrf_score", 0.0))),
                        )
                        for c in chunks[:3]
                    ]
            return ChatResponse(
                success=True,
                is_relevant=True,
                answer=answer,
                citations=citations,
                trace_id=trace_id
            )