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
        prompt: message,
        tools: selectedTools,
      }),
    });

    if (!response.body) {
      throw new Error("Response body is null.");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }
      const chunk = decoder.decode(value);
      onChunk(chunk);
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