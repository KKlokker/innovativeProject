function login() {
   let username = $("#username").val()
   if (username == "") {
       $("#error").text("Please enter a username")
       return
    }

    $.get("http://localhost:5000/internal/login?username=" + username, function(data) {
        // data is the response from the backend
        if (data.success) {
            // redirect to the home page
            localStorage.setItem("userid", data.userID)
            window.location.href = "/receipts.html"
        } else {
            // show error message
            $("#error").text(data.error)
        }
    }) 
}