import { showNotes } from "./showNotes.js";

export function showList(key) {
  return showNotes(key);
}
document
  .querySelector("searchBox")
  .addEventListener("onkeyup", showList("first"));
const searchResult = showNotes("subject");

console.log(searchResult);
