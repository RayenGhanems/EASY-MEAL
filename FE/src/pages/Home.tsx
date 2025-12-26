import { useNavigate } from "react-router-dom";

export default function Index() {
  const navigate = useNavigate();

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <h1 style={styles.title}>🍽️ Easy Meal</h1>
        <p style={styles.subtitle}>Turn your fridge into smart meal ideas</p>
      </header>
      <div style={styles.container}>
        <div style={styles.main}>
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>Scan your fridge</h2>
            <p style={styles.cardText}>
              Upload photos of your fridge or ingredients and let Easy Meal
              analyze what you have.
            </p>

            <button
              style={styles.primaryButton}
              onClick={() => navigate("/upload")}
            >
              📸 Upload fridge photos
            </button>

            <p style={styles.hint}>
              More features coming soon (recipes, shopping lists, preferences…)
            </p>
          </div>
        </div>
        <div style={styles.main}>
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>Get available recipes</h2>
            <p style={styles.cardText}>
              let Easy Meal suggest recipes based on the ingredients detected in
              your fridge.
            </p>

            <button
              style={styles.primaryButton}
              onClick={() => navigate("/recipes")}
            >
              🍳 Find recipes
            </button>

            <p style={styles.hint}>
              More features coming soon (recipes, shopping lists, preferences…)
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
const styles: Record<string, React.CSSProperties> = {
  page: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #f8fafc, #eef2f7)",
    display: "flex",
    flexDirection: "column",
  },
  container: {
    display: "flex",
    flexDirection: "row",
  },

  header: {
    padding: "40px 20px",
    textAlign: "center",
  },

  title: {
    fontSize: "2.5rem",
    margin: 0,
    color: "#111827",
  },

  subtitle: {
    marginTop: 10,
    fontSize: "1.1rem",
    color: "#6b7280",
  },

  main: {
    flex: 1,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },

  card: {
    backgroundColor: "#ffffff",
    borderRadius: 16,
    padding: 32,
    width: "100%",
    maxWidth: 420,
    boxShadow: "0 10px 30px rgba(0, 0, 0, 0.08)",
    textAlign: "center",
  },

  cardTitle: {
    fontSize: "1.5rem",
    marginBottom: 12,
    color: "#111827",
  },

  cardText: {
    fontSize: "1rem",
    color: "#4b5563",
    marginBottom: 24,
  },

  primaryButton: {
    width: "100%",
    padding: "14px 18px",
    fontSize: "1rem",
    fontWeight: 600,
    borderRadius: 10,
    border: "none",
    cursor: "pointer",
    background: "linear-gradient(135deg, #10b981, #059669)",
    color: "#ffffff",
    transition: "transform 0.15s ease, box-shadow 0.15s ease",
  },

  hint: {
    marginTop: 20,
    fontSize: "0.85rem",
    color: "#9ca3af",
  },
};
