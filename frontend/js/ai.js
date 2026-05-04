import { createClass, generateFlashcards } from "./api.js";

let currentClassId = null;

async function handleGenerateFlashcards() {
  const text = document.getElementById("flashcardInput").value;

  // create class ONLY once
  if (!currentClassId) {
    const newClass = await createClass("Demo Class", "Generated from UI");
    currentClassId = newClass.id;
  }

  const data = await generateFlashcards(currentClassId, text);

  let output = "";
  data.flashcards.forEach(card => {
    output += `<p><b>${card.question}</b><br>${card.answer}</p>`;
  });

  document.getElementById("flashcardOutput").innerHTML = output;
}

window.handleGenerateFlashcards = handleGenerateFlashcards;