import { useState } from "react";
import axios from "axios";

import {
  BrowserRouter,
  Routes,
  Route,
  useNavigate,
} from "react-router-dom";

import Dashboard from "./pages/Dashboard";

function AuthPage() {
  const navigate = useNavigate();

  const [isLogin, setIsLogin] = useState(false);

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async () => {
    try {
      if (isLogin) {
        const formData = new FormData();

        formData.append("username", email);
        formData.append("password", password);

        const response = await axios.post(
          "http://127.0.0.1:8000/login",
          formData
        );

        localStorage.setItem(
          "token",
          response.data.access_token
        );

        alert("Login successful");

        navigate("/dashboard");
      } else {
        await axios.post(
          "http://127.0.0.1:8000/signup",
          {
            username,
            email,
            password,
          }
        );

        alert("Signup successful");

        setIsLogin(true);
      }
    } catch (error) {
      console.log(error);

      if (error.response) {
        alert(error.response.data.detail);
      } else {
        alert("Backend connection failed");
      }
    }
  };

  return (
    <div
      style={{
        backgroundColor: "black",
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          width: "350px",
          padding: "30px",
          border: "1px solid gray",
          borderRadius: "10px",
        }}
      >
        <h1
          style={{
            color: "white",
            textAlign: "center",
            marginBottom: "30px",
          }}
        >
          {isLogin ? "Login" : "Signup"}
        </h1>

        {!isLogin && (
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) =>
              setUsername(e.target.value)
            }
            style={inputStyle}
          />
        )}

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) =>
            setEmail(e.target.value)
          }
          style={inputStyle}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
          style={inputStyle}
        />

        <button
          onClick={handleSubmit}
          style={buttonStyle}
        >
          {isLogin ? "Login" : "Signup"}
        </button>

        <button
          onClick={() => setIsLogin(!isLogin)}
          style={buttonStyle}
        >
          {isLogin
            ? "Create new account"
            : "Already have an account?"}
        </button>
      </div>
    </div>
  );
}

const inputStyle = {
  width: "100%",
  padding: "10px",
  marginBottom: "15px",
  backgroundColor: "#111",
  border: "1px solid gray",
  color: "white",
};

const buttonStyle = {
  width: "100%",
  padding: "10px",
  marginBottom: "10px",
  backgroundColor: "#222",
  color: "white",
  border: "none",
  cursor: "pointer",
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AuthPage />} />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;