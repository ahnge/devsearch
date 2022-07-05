let myTags = document.querySelectorAll("#my_tags");

for (let i = 0; i < myTags.length; i++) {
  let tag = myTags[i];
  tag.addEventListener("click", (e) => {
    e.preventDefault();
    id = e.target.dataset.tag;

    const deleteTag = async (e) => {
      const res = await fetch(`http://127.0.0.1:8000/api/remove-tag/`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: id }),
      });
      const data = await res.json();
    };
    deleteTag().then(e.target.remove());
  });
}
