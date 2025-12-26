import { useState, type FormEvent, type JSX } from "react";
import { Link } from "react-router-dom";
import "../style/signin.css";

interface SignUpResponse {
  message?: string;
  detail?: string;
}

export default function SignUp(): JSX.Element {
  const [password, setPassword] = useState<string>("");
  const [username, setUsername] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [success, setSuccess] = useState<string>("");

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      const data: SignUpResponse = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Sign up failed");
      }

      setSuccess("Account created successfully!");
      setUsername("");
      setPassword("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signin_div">
      <form onSubmit={handleSubmit} className="sign_in_form">
        <h2>Sign Up</h2>
        <input
          type="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
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
        <button type="submit" disabled={loading} className="signin_button">
          {loading ? "Creating account..." : "Sign Up"}
        </button>
        {error && <p>{error}</p>}
        {success && <p>{success}</p>}
        <div className="signup_link">
          Already have an account?
          <Link to="/signin"> Sign In</Link>
        </div>
      </form>
    </div>
  );
}
