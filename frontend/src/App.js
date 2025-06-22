import { useState } from "react";
import Students from "./components/Students";
import LoginForm from "./components/LoginForm";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <div className="App">
      <h1>Moringa Fullstack App</h1>
      {!loggedIn ? <LoginForm onLogin={() => setLoggedIn(true)} /> : <Students />}
    </div>
  );
}

export default App;
