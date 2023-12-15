let userid = localStorage.getItem("userid");

async function init() {
    if (userid == null) {
        window.location.href = "/"
    }
    // populate group table
    $("#groups-table").bootstrapTable("showLoading");
    let url = `http://localhost:5000/internal/${userid}/groups`;
    await $.get(url, function(data) {
        console.log(data);
        $("#groups-table").bootstrapTable("hideLoading");
        $("#groups-table").bootstrapTable("destroy");
        $("#groups-table").bootstrapTable({
            data: data,
            clickToSelect: true,
            singleSelect: true,
        });
        $("#groups-table > tbody > tr").click(viewGroup);
    });
}

function viewGroup(event) {
    // if the select is clicked, don't view the receipt
    if (event && $(event.target).is("select")) {
        return;
    }
    let group = $("#groups-table").bootstrapTable("getSelections")[0];
    let url = `http://localhost:5000/internal/${userid}/groupMembers/${group.id}`;
    $.get(url, function(data) {
        console.log(data);
        $("#group-content-table").bootstrapTable("destroy");
        $("#group-content-table").bootstrapTable({
            data: data,
            clickToSelect: true,
            singleSelect: true,
        });
    });
}

function createGroup() {
    let groupName = $("#groupName").val();
    let url = `http://localhost:5000/internal/${userid}/groups/${groupName}`;
    //put request
    $.ajax({
        url: url,
        type: "PUT",
        success: function(data) {
            console.log(data);
            init();
        }
    });
}

function deleteGroup() {
    let group = $("#groups-table").bootstrapTable("getSelections")[0];
    let url = `http://localhost:5000/internal/${userid}/groups/${group.id}`;
    $.ajax({
        url: url,
        type: "DELETE",
        success: function(data) {
            console.log(data);
            init();
        }
    });
}

function addUserToGroup() {
    let group = $("#groups-table").bootstrapTable("getSelections")[0];
    let user = $("#memberName").val();
    let url = `http://localhost:5000/internal/${userid}/groups/${group.id}/user/${user}`;
    $.post(url, function(data) {
        console.log(data);
        viewGroup(undefined);
    });
}

function removeUserFromGroup() {
    let group = $("#groups-table").bootstrapTable("getSelections")[0];
    let user = $("#group-members").val();
    let url = `http://localhost:5000/internal/${userid}/groups/${group.id}/user/${user}`;
    $.ajax({
        url: url,
        type: "DELETE",
        success: function(data) {
            console.log(data);
            viewGroup(undefined);
        }
    });
}


$(document).ready(init);
