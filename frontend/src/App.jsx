import { useState, useEffect, useRef } from "react";
import "./App.css";

const API_URL = "https://somya-ai-portfolio-api.onrender.com";

function App() {

  // =========================
  // MOBILE MENU
  // =========================

  const [menuOpen, setMenuOpen] = useState(false);

  // =========================
  // CHAT STATES
  // =========================

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);

  const [error, setError] = useState("");
  const [lastQuestion, setLastQuestion] = useState("");

  // =========================
  // PROJECT STATES
  // =========================

  const [expandedProject, setExpandedProject] = useState(null);

  // =========================
  // CHAT AUTO SCROLL
  // =========================

  const messagesEndRef = useRef(null);

  // =========================
  // SCROLL ANIMATION
  // =========================

  useEffect(() => {

    const sections = document.querySelectorAll(
      ".animate-on-scroll"
    );

    const observer = new IntersectionObserver(
      (entries) => {

        entries.forEach((entry) => {

          if (entry.isIntersecting) {
            entry.target.classList.add("show");
          }

        });

      },
      {
        threshold: 0.15,
      }
    );

    sections.forEach((section) => {
      observer.observe(section);
    });

    return () => {

      sections.forEach((section) => {
        observer.unobserve(section);
      });

    };

  }, []);

  // =========================
  // AUTO SCROLL CHAT
  // =========================

  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages, loading]);

  // =========================
  // TOGGLE PROJECT DETAILS
  // =========================

  const toggleProject = (projectNumber) => {

    setExpandedProject(
      expandedProject === projectNumber
        ? null
        : projectNumber
    );

  };

  // =========================
  // CLEAR CHAT
  // =========================

  const clearChat = () => {

    setMessages([]);
    setQuestion("");
    setLoading(false);

  };

  // =========================
  // ASK SUGGESTED QUESTION
  // =========================

  const askSuggestedQuestion = (suggestedQuestion) => {

    const userMessage = {
      role: "user",
      content: suggestedQuestion,
    };

    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage,
    ]);

    setQuestion("");
    setLoading(true);

    fetch(`${API_URL}/chat`, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        question: suggestedQuestion,
      }),
    })

      .then((response) => {

        if (!response.ok) {
          throw new Error("Server error");
        }

        return response.json();

      })

      .then((data) => {

        const aiMessage = {
          role: "ai",
          content: data.answer,
        };

        setMessages((previousMessages) => [
          ...previousMessages,
          aiMessage,
        ]);

      })

      .catch((error) => {

        console.error("AI Error:", error);

        setMessages((previousMessages) => [
          ...previousMessages,
          {
            role: "ai",
            content:
              "Sorry, I could not connect to the AI server.",
          },
        ]);

      })

      .finally(() => {

        setLoading(false);

      });

  };

  // =========================
  // ASK AI
  // =========================

  const askAI = async () => {

    if (!question.trim() || loading) {
      return;
    }

    const currentQuestion = question;

    const userMessage = {
      role: "user",
      content: currentQuestion,
    };

    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage,
    ]);

    setQuestion("");
    setLoading(true);

    try {

      const response = await fetch(
        `${API_URL}/chat`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            question: currentQuestion,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();

      const aiMessage = {
        role: "ai",
        content: data.answer,
      };

      setMessages((previousMessages) => [
        ...previousMessages,
        aiMessage,
      ]);

    } catch (error) {

      console.error("AI Error:", error);

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "ai",
          content:
            "Sorry, I could not connect to the AI server.",
        },
      ]);

    } finally {

      setLoading(false);

    }

  };

  // =========================
  // PAGE
  // =========================

  return (

    <div className="portfolio">

      {/* =========================
          FLOATING AI BUTTON
      ========================= */}

      <button
        className="floating-ai-button"
        onClick={() => setChatOpen(!chatOpen)}
      >
        🤖 Ask AI
      </button>


      {/* =========================
          NAVBAR
      ========================= */}

      <nav className="navbar">

        <a
          href="#home"
          className="logo"
          onClick={() => setMenuOpen(false)}
        >
          SK<span>.</span>
        </a>


        {/* MOBILE HAMBURGER */}

        <button
          className="hamburger"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle navigation menu"
        >
          ☰
        </button>


        {/* NAV LINKS */}

        <div
          className={`nav-links ${
            menuOpen ? "nav-open" : ""
          }`}
        >

          <a
            href="#about"
            onClick={() => setMenuOpen(false)}
          >
            About
          </a>

          <a
            href="#education"
            onClick={() => setMenuOpen(false)}
          >
            Education
          </a>

          <a
            href="#achievements"
            onClick={() => setMenuOpen(false)}
          >
            Achievements
          </a>

          <a
            href="#skills"
            onClick={() => setMenuOpen(false)}
          >
            Skills
          </a>

          <a
            href="#projects"
            onClick={() => setMenuOpen(false)}
          >
            Projects
          </a>

          <a
            href="#experience"
            onClick={() => setMenuOpen(false)}
          >
            Experience
          </a>

          <a
            href="#contact"
            onClick={() => setMenuOpen(false)}
          >
            Contact
          </a>

        </div>

      </nav>


      {/* =========================
          HERO
      ========================= */}

      <section id="home" className="hero">

        <div className="hero-content">

          <p className="intro">
            Hi, I'm
          </p>

          <h1>
            Somya Kashyap
          </h1>

          <h2>
            Software Development Engineer
          </h2>

          <p className="hero-tags">
            AI • Full Stack • Data Structures & Algorithms • Python
          </p>

          <p>
            Computer Science Engineering student passionate
            about software development, artificial intelligence,
            data structures and building practical solutions
            to real-world problems.
          </p>


          <div className="hero-buttons">

            <a href="#projects">

              <button>
                View My Projects
              </button>

            </a>


            <a
              href="/resume.pdf"
              target="_blank"
              rel="noreferrer"
            >

              <button className="secondary-button">
                Resume ↗
              </button>

            </a>

          </div>

        </div>

      </section>


      {/* =========================
          ABOUT
      ========================= */}

      <section
        id="about"
        className="section about-section animate-on-scroll"
      >

        <div className="about-header">

          <p className="section-label">
            ABOUT ME
          </p>

          <h2>
            Building software with curiosity.
          </h2>

        </div>


        <div className="about-grid">

          <div className="about-text">

            <p>
              I'm a Computer Science Engineering student passionate
              about software development, artificial intelligence,
              data structures and problem solving.
            </p>

            <p>
              I enjoy turning ideas into practical projects and
              continuously learning new technologies. My goal is to
              build software that is useful, thoughtful and technically
              interesting.
            </p>

          </div>


          <div className="about-card">

            <p className="about-card-label">
              CURRENTLY
            </p>

            <h3>
              Learning. Building. Shipping.
            </h3>

            <p>
              Exploring full-stack development, AI-powered applications,
              system design and data structures while building projects
              that challenge me to learn by doing.
            </p>

          </div>

        </div>

      </section>


      {/* =========================
          EDUCATION
      ========================= */}

      <section
        id="education"
        className="section education-section animate-on-scroll"
      >

        <p className="section-label">
          EDUCATION
        </p>

        <h2>
          Academic foundation.
        </h2>

        <div className="education-card">

          <div>

            <p className="education-type">
              BACHELOR OF TECHNOLOGY
            </p>

            <h3>
              Computer Science & Engineering
            </h3>

            <p className="education-institute">
              PSIT Kanpur
            </p>

          </div>


          <div className="education-details">

            <p>
              AKTU, Lucknow
            </p>

            <p>
              2024 – 2028
            </p>

          </div>

        </div>

      </section>


      {/* =========================
          CERTIFICATIONS
      ========================= */}

      <section
        id="achievements"
        className="section achievements-section"
      >

        <p className="section-label">
          CERTIFICATIONS & ACHIEVEMENTS
        </p>

        <h2>
          Learning beyond the classroom.
        </h2>

        <p className="section-text">
          Certifications and learning experiences that have
          strengthened my skills in AI, sustainability, and technology.
        </p>


        <div className="certifications-grid">

          {/* Certificate 1 */}

          <div className="certificate-card animate-on-scroll">

            <div className="certificate-image">

              <img
                src="/certificates/ai-skills-passport.png"
                alt="AI Skills Passport certificate"
              />

            </div>


            <div className="certificate-info">

              <p className="certificate-type">
                CERTIFICATION
              </p>

              <h3>
                AI Skills Passport
              </h3>

              <p>
                EY × Microsoft
              </p>

              <span>
                2026
              </span>

            </div>

          </div>


          {/* Certificate 2 */}

          <div className="certificate-card animate-on-scroll">

            <div className="certificate-image">

              <img
                src="/certificates/green-skills-ai.png"
                alt="Green Skills and Applied AI certificate"
              />

            </div>


            <div className="certificate-info">

              <p className="certificate-type">
                BOOTCAMP
              </p>

              <h3>
                Green Skills & Applied AI for Climate Action
              </h3>

              <p>
                Microsoft × 1M1B
              </p>

              <span>
                2026
              </span>

            </div>

          </div>


          {/* Certificate 3 */}

          <div className="certificate-card animate-on-scroll">

            <div className="certificate-image">

              <img
                src="/certificates/certificate-3.png"
                alt="Certificate"
              />

            </div>


            <div className="certificate-info">

              <p className="certificate-type">
                CERTIFICATION
              </p>

              <h3>
                Your Certificate Name
              </h3>

              <p>
                Issuing Organization
              </p>

              <span>
                2026
              </span>

            </div>

          </div>

        </div>

      </section>


      {/* =========================
          SKILLS
      ========================= */}

      <section
        id="skills"
        className="section skills-section animate-on-scroll"
      >

        <p className="section-label">
          TECHNOLOGIES
        </p>

        <h2>
          Skills & Tools
        </h2>

        <p className="section-text skills-intro">
          A growing toolkit of languages, technologies, and
          computer science concepts I use while building projects.
        </p>


        <div className="skills-categories">


          {/* PROGRAMMING */}

          <div className="skill-category">

            <div className="skill-category-header">

              <span className="skill-category-number">
                01
              </span>

              <h3>
                Programming
              </h3>

            </div>

            <div className="skill-tags">

              <span>C++</span>
              <span>Python</span>
              <span>JavaScript</span>

            </div>

          </div>


          {/* FRONTEND */}

          <div className="skill-category">

            <div className="skill-category-header">

              <span className="skill-category-number">
                02
              </span>

              <h3>
                Frontend
              </h3>

            </div>

            <div className="skill-tags">

              <span>HTML</span>
              <span>CSS</span>
              <span>React</span>

            </div>

          </div>


          {/* BACKEND & DATA */}

          <div className="skill-category">

            <div className="skill-category-header">

              <span className="skill-category-number">
                03
              </span>

              <h3>
                Backend & Data
              </h3>

            </div>

            <div className="skill-tags">

              <span>FastAPI</span>
              <span>SQL</span>
              <span>Pandas</span>
              <span>NumPy</span>

            </div>

          </div>


          {/* AI & COMPUTER SCIENCE */}

          <div className="skill-category">

            <div className="skill-category-header">

              <span className="skill-category-number">
                04
              </span>

              <h3>
                AI & Computer Science
              </h3>

            </div>

            <div className="skill-tags">

              <span>Data Structures & Algorithms</span>
              <span>Machine Learning</span>
              <span>RAG</span>

            </div>

          </div>


          {/* TOOLS */}

          <div className="skill-category">

            <div className="skill-category-header">

              <span className="skill-category-number">
                05
              </span>

              <h3>
                Tools
              </h3>

            </div>

            <div className="skill-tags">

              <span>Git</span>
              <span>GitHub</span>

            </div>

          </div>

        </div>

      </section>


      {/* =========================
          PROJECTS
      ========================= */}

      <section
        id="projects"
        className="section projects-section animate-on-scroll"
      >

        <p className="section-label">
          PROJECTS
        </p>

        <h2>
          Things I've built.
        </h2>

        <p className="section-text">
          A collection of projects where I experiment with
          software development, AI, data, and machine learning.
        </p>


        <div className="projects-grid">


          {/* =========================
              AMAZON COPILOT
          ========================= */}

          <article className="project-card">

            <div className="project-top">

              <span className="project-number">
                01
              </span>

              <span className="project-type">
                AI / RAG
              </span>

            </div>


            <h3>
              Amazon Copilot
            </h3>

            <p>
              An AI-powered shopping assistant designed to analyze
              product information, summarize reviews, compare products,
              and generate useful shopping insights.
            </p>


            <div className="project-tech">

              <span>Python</span>
              <span>FastAPI</span>
              <span>RAG</span>
              <span>AI</span>

            </div>


            <div className="project-buttons">

              <a
                href="https://github.com/somyakashyapjha-afk/amazon-copilot"
                target="_blank"
                rel="noreferrer"
                className="project-button"
              >
                GitHub ↗
              </a>


              <button
                className="project-button secondary"
                onClick={() => toggleProject(1)}
              >
                {expandedProject === 1
                  ? "Hide Details"
                  : "View Details"}
              </button>

            </div>


            {expandedProject === 1 && (

              <div className="project-details">

                <div className="project-detail-block">

                  <h4>
                    Overview
                  </h4>

                  <p>
                    Amazon Copilot is an AI-powered shopping
                    assistant designed to help users understand
                    product information and make sense of customer
                    reviews.
                  </p>

                </div>


                <div className="project-detail-block">

                  <h4>
                    Key Features
                  </h4>

                  <ul>

                    <li>
                      Product review summarization
                    </li>

                    <li>
                      AI-powered product insights
                    </li>

                    <li>
                      Retrieval-Augmented Generation
                    </li>

                    <li>
                      FastAPI backend
                    </li>

                  </ul>

                </div>


                <div className="project-detail-block">

                  <h4>
                    Tech Stack
                  </h4>

                  <p>
                    Python · FastAPI · RAG · AI
                  </p>

                </div>

              </div>

            )}

          </article>


          {/* =========================
              CAMPUS SUSTAINABILITY
          ========================= */}

          <article className="project-card">

            <div className="project-top">

              <span className="project-number">
                02
              </span>

              <span className="project-type">
                DATA / ML
              </span>

            </div>


            <h3>
              Campus Sustainability Dashboard
            </h3>

            <p>
              A data analysis and visualization project for monitoring
              campus sustainability metrics, detecting anomalies,
              and identifying useful patterns from environmental data.
            </p>


            <div className="project-tech">

              <span>Python</span>
              <span>Pandas</span>
              <span>NumPy</span>
              <span>Scikit-learn</span>
              <span>Power BI</span>

            </div>


            <div className="project-buttons">

              <a
                href="https://github.com/somyakashyapjha-afk/campus-sustainability-dashboard"
                target="_blank"
                rel="noreferrer"
                className="project-button"
              >
                GitHub ↗
              </a>


              <button
                className="project-button secondary"
                onClick={() => toggleProject(2)}
              >
                {expandedProject === 2
                  ? "Hide Details"
                  : "View Details"}
              </button>

            </div>


            {expandedProject === 2 && (

              <div className="project-details">

                <div className="project-detail-block">

                  <h4>
                    Overview
                  </h4>

                  <p>
                    A sustainability analytics project that
                    analyzes campus environmental data to identify
                    patterns, anomalies, and potential areas for
                    improvement.
                  </p>

                </div>


                <div className="project-detail-block">

                  <h4>
                    Key Features
                  </h4>

                  <ul>

                    <li>
                      Environmental data analysis
                    </li>

                    <li>
                      Sustainability metric tracking
                    </li>

                    <li>
                      Anomaly detection
                    </li>

                    <li>
                      Data visualization
                    </li>

                  </ul>

                </div>


                <div className="project-detail-block">

                  <h4>
                    Tech Stack
                  </h4>

                  <p>
                    Python · Pandas · NumPy · Scikit-learn · Power BI
                  </p>

                </div>

              </div>

            )}

          </article>


          {/* =========================
              TALENT MARKET INTELLIGENCE
          ========================= */}

          <article className="project-card">

            <div className="project-top">

              <span className="project-number">
                03
              </span>

              <span className="project-type">
                DATA / ANALYTICS
              </span>

            </div>


            <h3>
              Talent Market Intelligence Platform
            </h3>

            <p>
              An end-to-end data platform that transforms talent data
              through ETL and feature engineering, segments candidates,
              and presents insights through an interactive dashboard.
            </p>


            <div className="project-tech">

              <span>Python</span>
              <span>ETL</span>
              <span>K-Means</span>
              <span>Plotly</span>
              <span>Streamlit</span>

            </div>


            <div className="project-buttons">

              <a
                href="https://github.com/somyakashyapjha-afk/Talent-Market-Intelligence-Platform"
                target="_blank"
                rel="noreferrer"
                className="project-button"
              >
                GitHub ↗
              </a>


              <button
                className="project-button secondary"
                onClick={() => toggleProject(3)}
              >
                {expandedProject === 3
                  ? "Hide Details"
                  : "View Details"}
              </button>

            </div>


            {expandedProject === 3 && (

              <div className="project-details">

                <div className="project-detail-block">

                  <h4>
                    Overview
                  </h4>

                  <p>
                    An end-to-end talent analytics platform that
                    processes talent data, performs feature engineering,
                    segments candidates, and presents insights through
                    an interactive dashboard.
                  </p>

                </div>


                <div className="project-detail-block">

                  <h4>
                    Key Features
                  </h4>

                  <ul>

                    <li>
                      Data preprocessing and ETL
                    </li>

                    <li>
                      Feature engineering
                    </li>

                    <li>
                      Candidate segmentation using K-Means
                    </li>

                    <li>
                      Interactive data visualization
                    </li>

                  </ul>

                </div>


                <div className="project-detail-block">

                  <h4>
                    Tech Stack
                  </h4>

                  <p>
                    Python · ETL · K-Means · Plotly · Streamlit
                  </p>

                </div>

              </div>

            )}

          </article>

        </div>

      </section>


      {/* =========================
          EXPERIENCE
      ========================= */}

      <section
        id="experience"
        className="section experience-section animate-on-scroll"
      >

        <p className="section-label">
          EXPERIENCE
        </p>

        <h2>
          Where I've been learning and building.
        </h2>


        <div className="experience-card">

          <div className="experience-header">

            <div>

              <p className="experience-type">
                INTERNSHIP
              </p>

              <h3>
                AI & Green Skills Intern
              </h3>

              <p className="company">
                Microsoft × 1M1B
              </p>

            </div>

            <p className="experience-date">
              2026
            </p>

          </div>


          <div className="experience-divider"></div>


          <ul>

            <li>
              Worked on applied AI and sustainability-focused
              projects.
            </li>

            <li>
              Explored practical applications of artificial
              intelligence to real-world problems.
            </li>

            <li>
              Developed technical and problem-solving skills
              through project-based work.
            </li>

          </ul>

        </div>

      </section>


      {/* =========================
          FLOATING AI CHAT
      ========================= */}

      {chatOpen && (

        <div className="floating-chat">


          {/* CHAT HEADER */}

          <div className="floating-chat-header">

            <div>

              <strong>
                🤖 Somya AI
              </strong>

              <p>
                Ask me anything
              </p>

            </div>


            <div className="chat-header-actions">

              <button
                className="new-chat-button"
                onClick={clearChat}
                title="Start a new chat"
              >
                ↻
              </button>


              <button
                className="close-chat"
                onClick={() => setChatOpen(false)}
                title="Close chat"
              >
                ×
              </button>

            </div>

          </div>


          {/* CHAT MESSAGES */}

          <div className="floating-chat-messages">

            {messages.length === 0 && (

              <div className="chat-welcome">

                <div className="chat-message ai-message">

                  <strong>
                    🤖 AI
                  </strong>

                  <p>
                    Hi! I'm Somya's AI assistant.
                    Ask me about her projects, skills,
                    experience, or education.
                  </p>

                </div>


                <div className="chat-suggestions">

                  <p className="suggestions-title">
                    Try asking:
                  </p>


                  <button
                    onClick={() =>
                      askSuggestedQuestion(
                        "What projects has Somya built?"
                      )
                    }
                  >
                    What projects has Somya built?
                  </button>


                  <button
                    onClick={() =>
                      askSuggestedQuestion(
                        "What are Somya's technical skills?"
                      )
                    }
                  >
                    What are Somya's technical skills?
                  </button>


                  <button
                    onClick={() =>
                      askSuggestedQuestion(
                        "Tell me about Amazon Copilot"
                      )
                    }
                  >
                    Tell me about Amazon Copilot
                  </button>


                  <button
                    onClick={() =>
                      askSuggestedQuestion(
                        "What experience does Somya have?"
                      )
                    }
                  >
                    What experience does Somya have?
                  </button>

                </div>

              </div>

            )}


            {messages.map((message, index) => (

              <div
                key={index}
                className={
                  message.role === "user"
                    ? "chat-message user-message"
                    : "chat-message ai-message"
                }
              >

                <strong>
                  {message.role === "user"
                    ? "You"
                    : "🤖 AI"}
                </strong>

                <p>
                  {message.content}
                </p>

              </div>

            ))}


            {loading && (

              <div className="chat-message ai-message typing-message">

                <strong>
                  🤖 AI
                </strong>

                <div className="typing-indicator">

                  <span></span>
                  <span></span>
                  <span></span>

                </div>

              </div>

            )}


            {/* AUTO SCROLL TARGET */}

            <div ref={messagesEndRef} />

          </div>


          {/* CHAT INPUT */}

          <div className="floating-chat-input">

            <input
              type="text"
              placeholder="Ask something..."
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              onKeyDown={(event) => {

                if (event.key === "Enter") {
                  askAI();
                }

              }}
            />


            <button
              onClick={askAI}
              disabled={loading}
            >
              Send
            </button>

          </div>

        </div>

      )}


      {/* =========================
          CONTACT
      ========================= */}

      <section
        id="contact"
        className="section contact animate-on-scroll"
      >

        <p className="section-label">
          CONTACT
        </p>

        <h2>
          Let's build something.
        </h2>

        <p className="section-text">
          I'm always interested in learning, building new
          projects and connecting with people working in
          software and AI.
        </p>


        <div className="contact-links">

          <a
            href="mailto:your-email@gmail.com"
            className="contact-link"
          >
            Email Me ↗
          </a>


          <a
            href="https://github.com/somyakashyapjha-afk"
            target="_blank"
            rel="noreferrer"
            className="contact-link"
          >
            GitHub ↗
          </a>


          <a
            href="https://www.linkedin.com/"
            target="_blank"
            rel="noreferrer"
            className="contact-link"
          >
            LinkedIn ↗
          </a>

        </div>

      </section>


      {/* =========================
          FOOTER
      ========================= */}

      <footer className="footer">

        <p>
          © 2026 Somya Kashyap
        </p>

        <p>
          Built with React + FastAPI + AI
        </p>

      </footer>

    </div>

  );

}

export default App;