import { useState, type FormEvent, type JSX } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import "../style/signin.css";

interface LoginResponse {
  access_token?: string;
  token_type?: string;
  detail?: string;
}

export default function SignIn(): JSX.Element {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/auth/signin", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // if using HttpOnly cookies
        body: JSON.stringify({ username, password }),
      });

      const data: LoginResponse = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Invalid credentials");
      }

      // If using header-based JWT:
      // localStorage.setItem("access_token", data.access_token!);
      navigate("/home", { replace: true });
      console.log("Logged in successfully", data);

      // navigate("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signin_div">
      <form onSubmit={handleSubmit} className="sign_in_form">
        <h2 className="signin_lable">Sign In</h2>
        <input
          type="email"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Email"
          required
          className="signin_inputs"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
          className="signin_inputs"
        />
        <div className="div_button">
          <button type="submit" disabled={loading} className="signin_button">
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </div>

        {error && <p>{error}</p>}
        <div className="signup_link">
          Do not have an account?
          <Link to="/signup"> Sign Up</Link>
        </div>
      </form>
    </div>
  );
}
