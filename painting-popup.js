function Popup(title, author, file, description, dir) {
  $("#painting-title").text(title)
  $("#painting-author").text(author)
  $("#painting-description").text(description)
  $("#painting").attr("src", "paintings/" + file + ".jpg")
  if (dir === "V") {
    $("#modal-dia").removeClass("modal-lg");
  } else {
    $("#modal-dia").addClass("modal-lg");
  }
  $('#infoModal').modal('show');
}
function ShowAbout() {
  $('#aboutModal').modal('show');
}
function ShowArtistModal() {
  $('#artistModal').modal('show');
}
