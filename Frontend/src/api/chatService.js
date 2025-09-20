// Make sure you have a .env file in your Frontend folder with:
// REACT_APP_API_URL=http://127.0.0.1:8000/api/v1
const API_URL = `${process.env.REACT_APP_API_URL}/chat`;

export const streamMessageFromBackend = async (message, selectedTools, onChunk) => {
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify({
        // Note: Your backend schema uses 'query', not 'prompt'. Let's match it.
        session_id: 'some-unique-session-id', // You can generate this
        query: message,
        include_visualization: selectedTools.includes('graph'), // Example logic
        // language and context can be added here if needed
      }),
    });

    if (!response.body) {
      throw new Error("Response body is null.");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    // Instead of processing line by line, process larger chunks:
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value, { stream: true });
      
      // Process immediately instead of buffering
      if (chunk.startsWith('data: ')) {
        const jsonString = chunk.substring(6);
        try {
          const jsonObject = JSON.parse(jsonString);
          onChunk(jsonObject);
        } catch (e) {
          onChunk(chunk.substring(6));
        }
      } else if (chunk.trim()) {
        onChunk(chunk);
      }
    }

  } catch (error) {
    console.error("Error communicating with the backend:", error);
    onChunk({
      type: 'error',
      text: "Sorry, I'm having trouble connecting to the server. Please try again later.",
      errorDetails: error.message
    });
  }
};