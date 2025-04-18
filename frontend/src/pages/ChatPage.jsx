import React, { useState } from "react"
import { MessageInput } from "../components/ui/message-input"
import { PromptSuggestions } from "../components/ui/prompt-suggestions"

export default function ChatPage() {
  const [message, setMessage] = useState("")
  const [files, setFiles] = useState([])
  const [messages, setMessages] = useState([]) // To store chat messages

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim()) {
      // Add the message to our messages array
      const newMessage = { role: "user", content: message }
      setMessages([...messages, newMessage])
      
      console.log("Submitted Message:", message)
      console.log("Attached Files:", files)
      setMessage("") // Clear input
      setFiles([])   // Clear files
    }
  }

  // This function will add a suggestion to the message input
  const appendMessage = (newMessage) => {
    setMessage(newMessage.content)
  }

  const handleTranscription = async (audioBlob) => {
    // Example placeholder: Convert audioBlob to text
    const transcribedText = "Sample transcribed text"
    return transcribedText
  }

  // Example suggestions
  const promptSuggestions = [
    "Help me get the algorithm for this problem",
    "What is the time and space comlexity",
    "Can you help me solve this question "
  ]

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto">
      {/* Chat Container */}
      <div className="flex-1 flex flex-col justify-between overflow-hidden">
        
        {/* Empty State with Centered Suggestions */}
        {messages.length === 0 ? (
          <div className="flex-1 flex items-center justify-center px-4">
            <div className="w-full max-w-3xl">
              <PromptSuggestions
                label="How can I help you today?"
                append={appendMessage}
                suggestions={promptSuggestions}
              />
            </div>
          </div>
        ) : (
          /* Chat Messages Display Area */
          <div className="flex-1 overflow-y-auto py-4 px-4">
            {messages.map((msg, index) => (
              <div 
                key={index} 
                className={`mb-4 flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div 
                  className={`max-w-3/4 rounded-lg p-3 ${
                    msg.role === "user" 
                      ? "bg-blue-500 text-white rounded-br-none" 
                      : "bg-gray-100 text-gray-800 rounded-bl-none"
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Message Input Area - Fixed at bottom */}
        <div className="border-t bg-black p-4">
          <form onSubmit={handleSubmit} className="flex flex-col gap-2">
            <MessageInput
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              allowAttachments={true}
              files={files}
              setFiles={setFiles}
              isGenerating={false}
              stop={() => console.log("Stop generation")}
              transcribeAudio={handleTranscription}
              placeholder="Type your message here..."
            />
          </form>
        </div>
      </div>
    </div>
  )
}