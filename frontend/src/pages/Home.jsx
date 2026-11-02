import Navbar from "../components/Navbar/Navbar";
import ActionCard from "../components/ActionCard/ActionCard";
import Footer from "../components/Footer/Footer";
import "./Home.css";

function Home() {
  return (
    <div className="home-page">
      <Navbar />

      <main className="home-container">
        <div className="hero">
          <span className="hero-label">👻 YOUR SEARCH STARTS HERE</span>

          <h1>
            Lost something?
            <br />
            <span>Let's find it.</span>
          </h1>

          <p>
            Don't just search for what's lost.
            Discover where it might be.
          </p>
        </div>

        <div className="action-cards">
          <ActionCard
            to="/report/lost"
            variant="lost-card"
            icon="🔍"
            title="I Lost Something"
            text="Tell us what you lost. We'll search for possible matches and help investigate."
            cta="Find my item →"
          />

          <ActionCard
            to="/report/found"
            variant="found-card"
            icon="🎒"
            title="I Found Something"
            text="Report an item you found. We may help connect it with its owner."
            cta="Report found item →"
          />
        </div>

        <Footer />
      </main>
    </div>
  );
}

export default Home;