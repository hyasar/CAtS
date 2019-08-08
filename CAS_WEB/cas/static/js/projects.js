// let project_ids = []
// let control_lists = {}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        var c = cookies[i].trim();
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length);
        }
    }
    return "unknown";
}

function deleteProject(project_id, project_name) {
    var result = confirm("Are you sure you want to delete " + project_name + "?");
    if (result) {
        //Logic to delete the item
        $.ajax({
            url: "/delete",
            type: "POST",
            data: "project_id=" + project_id + "&csrfmiddlewaretoken=" + getCSRFToken(),
            success: function (message) {
                location.reload();
                alert(message);
            }
        });

    }
}

