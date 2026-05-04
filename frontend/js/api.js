export async function createClass(name, description) {
  const res = await fetch("http://127.0.0.1:8000/classes", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ name, description })
  });

  return res.json();
}
export async function generateFlashcards(class_id, source_text) {
  const res = await fetch("http://127.0.0.1:8000/flashcards/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      class_id: class_id,
      source_text: source_text
    })
  });

  return res.json();
}