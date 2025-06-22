import "./Students.css";
import { useEffect, useState } from "react";

export default function Students() {
  const [students, setStudents] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchStudents() {
      try {
        const response = await fetch("/students", {
          credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to fetch students");
        const data = await response.json();
        setStudents(data);
      } catch (err) {
        setError(err.message);
      }
    }

    fetchStudents();
  }, []);

  return (
    <div className="students-container">
      <div className="list-group">
        <h1
          className="list-group-item list-group-item-action active"
          aria-current="true"
        >
          Moringa's Students
        </h1>

        {error ? (
          <p className="list-group-item text-danger">Error: {error}</p>
        ) : (
          students.map((student) => (
            <a
              key={student.id}
              href={`/students/${student.id}`}
              className="list-group-item list-group-item-action"
            >
              {student.name}
            </a>
          ))
        )}
      </div>
    </div>
  );
}
