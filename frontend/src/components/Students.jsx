import { useEffect, useState } from "react";

export default function Students() {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    async function fetchStudents() {
      const response = await fetch("http://127.0.0.1:5555/students");
      setStudents(await response.json());
    }
    fetchStudents();
  }, []);
  return (
    <>
      <div className="list-group">
        <h1
          className="list-group-item list-group-item-action active"
          aria-current="true"
        >
          Moringa's students
        </h1>
        {students.map((student) => (
          <a
            key={student.id}
            href={`/students/${student.id}`}
            className="list-group-item list-group-item-action"
          >
            {student.name}
          </a>
        ))}
      </div>
    </>
  );
}
