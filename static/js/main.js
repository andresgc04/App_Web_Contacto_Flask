const btnDelete = document.querySelectorAll(".btn-delete");

if (btnDelete) {
  const btnDeleteArray = Array.from(btnDelete);

  btnDeleteArray.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      if (
        !confirm("Estas seguro de querer eliminar este elemento seleccionado?")
      ) {
        e.preventDefault();
      }
    });
  });
}
