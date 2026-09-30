import React, { useState } from "react";



function App() {
    const [messages, setMessages] = useState([
        { role: 'assistant', question: 'Hello! Ask me about your docs.', citations: [] }
    ]);
    const [inputText, setInputText] = useState("");
    const [isThinking, setIsThinking] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!inputText.trim()) return;
        
        const userQuery = inputText;
        const newUserMessage = { role: 'user', question: userQuery, citations: [] };

        setMessages([...messages, newUserMessage]);
        setInputText('');
        setIsThinking(true);

        try {
            const response = await fetch('http://127.0.0.1:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json'},
                body: JSON.stringify({
                    question: userQuery
                })
            });

            const data = await response.json();
            console.log("Raw Python Data Return:", data);

            const newAiMessage = {
                role: 'assistant',
                question: data.question,
                answer: data.answer,
                citations: data.citations || []
            };

            setMessages((prev) => [...prev, newAiMessage]);
        } catch (error) {
            setMessages((prev) => [
                ...prev,
                { role: 'assistant', answer: 'Failed to communicate with the document brain.'}
            ]);
        } finally {
            setIsThinking(false);
        }
    };

    return (
        <div>
            { messages.map((msg, index) => (
                <div key={index}>
                    <p>{msg.answer}</p>

                                {msg.citations && msg.citations.length > 0 && (
                <small style={{ color: 'gray' }}>
                    Citations: {msg.citations.map(c => `Page ${c.page_number}`).join(', ')}
                </small>
                )}
                </div>
            ))}

            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Ask about the docs..."
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                />
                <button type="submit">Send</button>
            </form>        
        </div>
        );
    }

export default App;