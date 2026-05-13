import { useState } from "react";
import axios from "axios";
function Dashboard() {

  const [file, setFile] = useState(null);

  const [message, setMessage] = useState("");

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [videos, setVideos] = useState([]);

  const [moduleName, setModuleName] = useState("");

  const [moduleId, setModuleId] = useState(null);

  const [chatHistory, setChatHistory] = useState([]);

  const [summary, setSummary] = useState("");

  const [url, setUrl] = useState("");

  const token = localStorage.getItem("token");

  // CREATE MODULE
  const createModule = async () => {

    try {

      const response = await axios.post(
        "http://localhost:8000/modules",
        {
          title: moduleName
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      const module_id =
        response.data.id ||
        response.data.module_id;

      setModuleId(module_id);

      alert("Module created successfully");

    } catch (error) {

      console.error(error);

      alert("Module creation failed");

    }

  };

  // FILE UPLOAD
  const handleUpload = async () => {

    if (!moduleId) {

      setMessage("Please create a module first");

      return;

    }

    if (!file) {

      setMessage("Please select a file");

      return;

    }

    try {

      setMessage("Uploading file...");

      const formData = new FormData();

      formData.append("file", file);

      const response = await axios.post(
        `http://localhost:8000/upload/${moduleId}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setMessage(
        `File uploaded successfully: ${response.data.filename}`
      );

    } catch (error) {

      console.error(error);

      setMessage("Upload failed");

    }

  };

  // GENERATE SUMMARY
  const generateSummary = async () => {

    try {

      setSummary("Generating summary...");

      const response = await axios.get(
        "http://localhost:8000/summary"
      );

      setSummary(response.data.summary);

    } catch (error) {

      console.error(error);

      setSummary("Summary generation failed");

    }

  };

  // ASK AI
  const askQuestion = async () => {

    try {

      setAnswer("Generating answer...");

      const response = await axios.post(
        "http://localhost:8000/chat",
        {
          question: question,
          url: url
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setAnswer(response.data.answer);

      setVideos(response.data.related_videos || []);

      setChatHistory((prev) => [
        ...prev,
        {
          question: question,
          answer: response.data.answer
        }
      ]);

    } catch (error) {

      console.error(error);

      setAnswer("Something went wrong");

    }

  };

  return (

    <div
      style={{
        backgroundColor: "#0f172a",
        minHeight: "100vh",
        color: "white",
        padding: "40px",
        fontFamily: "Arial"
      }}
    >

      <h1
        style={{
          fontSize: "40px",
          marginBottom: "20px"
        }}
      >
        Insight LM
      </h1>

      <p>
        <strong>Current Module ID:</strong> {moduleId}
      </p>

      <hr />

      {/* MODULE */}

      <h2>Create Module</h2>

      <input
        type="text"
        placeholder="Enter module name"
        value={moduleName}
        onChange={(e) => setModuleName(e.target.value)}
        style={inputStyle}
      />

      <br />

      <button
        onClick={createModule}
        style={buttonStyle}
      >
        Create Module
      </button>

      <hr />

      {/* FILE */}

      <h2>Upload PDF</h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br />
      <br />

      <button
        onClick={handleUpload}
        style={buttonStyle}
      >
        Upload File
      </button>

      <p>{message}</p>

      <hr />

      {/* URL */}

      <h2>Website URL</h2>

      <input
        type="text"
        placeholder="Paste website/article URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={inputStyle}
      />

      <hr />

      {/* SUMMARY */}

      <h2>Generate Summary</h2>

      <button
        onClick={generateSummary}
        style={buttonStyle}
      >
        Generate Summary
      </button>

      <p>{summary}</p>

      <hr />

      {/* AI */}

      <h2>Ask AI</h2>

      <input
        type="text"
        placeholder="Ask question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={inputStyle}
      />

      <br />

      <button
        onClick={askQuestion}
        style={buttonStyle}
      >
        Ask AI
      </button>

      <br />
      <br />

      <div
        style={cardStyle}
      >
        <h3>AI Answer</h3>

        <p>{answer}</p>
      </div>

      <hr />

      {/* HISTORY */}

      <h2>Chat History</h2>

      {
        chatHistory.map((chat, index) => (

          <div
            key={index}
            style={cardStyle}
          >

            <p>
              <strong>Question:</strong>
            </p>

            <p>{chat.question}</p>

            <p>
              <strong>Answer:</strong>
            </p>

            <p>{chat.answer}</p>

          </div>

        ))
      }

      <hr />

      {/* VIDEOS */}

      <h2>Related Videos</h2>

      {
        videos.map((video, index) => (

          <div
            key={index}
            style={cardStyle}
          >

            <a
              href={video.link}
              target="_blank"
              rel="noreferrer"
              style={{
                color: "#60a5fa"
              }}
            >
              {video.title}
            </a>

          </div>

        ))
      }

    </div>

  );

}

const inputStyle = {
  width: "400px",
  padding: "12px",
  marginBottom: "20px",
  borderRadius: "10px",
  border: "none",
  fontSize: "16px"
};

const buttonStyle = {
  padding: "12px 20px",
  backgroundColor: "#7c3aed",
  color: "white",
  border: "none",
  borderRadius: "10px",
  cursor: "pointer",
  fontSize: "16px"
};

const cardStyle = {
  backgroundColor: "#1e293b",
  padding: "20px",
  borderRadius: "10px",
  marginBottom: "20px"
};

export default Dashboard;