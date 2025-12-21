import { useState, type FormEvent, type JSX } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

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
    <div style={styles.container}>
      <form onSubmit={handleSubmit} style={styles.form}>
        <h2>Sign In</h2>

        <input
          type="email"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Email"
          required
          style={styles.input}
        />

        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
          style={styles.input}
        />

        <button type="submit" disabled={loading} style={styles.button}>
          {loading ? "Signing in..." : "Sign In"}
        </button>

        {error && <p style={styles.error}>{error}</p>}
      </form>
      Create an account?
      <Link to="/signup"> Sign Up</Link>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
  },
  form: {
    width: 300,
    padding: 20,
    border: "1px solid #ddd",
    borderRadius: 6,
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },
  input: {
    padding: 10,
    fontSize: 14,
  },
  button: {
    padding: 10,
    fontSize: 14,
    cursor: "pointer",
  },
  error: {
    color: "red",
    fontSize: 13,
  },
};
