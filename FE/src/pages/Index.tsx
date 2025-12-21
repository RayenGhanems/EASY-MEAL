export default function Index() {
  return (
    <div
      style={{
        padding: "20px",
        textAlign: "center",
        width: "100%",
        height: "100%",
      }}
    >
      <h1>Welcome to Easy Meal</h1>
      <p>Your solution for easy meal planning!</p>
      <a href="/Signup">
        <button
          style={{
            padding: "10px 20px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          Get Started
        </button>
      </a>
    </div>
  );
}
