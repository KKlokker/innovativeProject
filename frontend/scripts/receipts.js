let userid;
let groupUsers = [];
let groups = [];

async function init() {
    userid = localStorage.getItem("userid")
    if (userid == null) {
        window.location.href = "/"
    }
    populateGroupUsers();
    populateGroups();
    $("#receipts-table").bootstrapTable("showLoading");
    await $.get("http://localhost:5000/internal/" + userid + "/receipts", function(data) {
        $("#receipts-table").bootstrapTable("hideLoading");
        $("#receipts-table").bootstrapTable({
            data: data,
            clickToSelect: true,
            singleSelect: true,
        });
        $("#receipts-table > tbody > tr").click(viewReceipt);
        // create selection event listeners
        $("#receipts-table > tbody > tr > td > select").change(function(event) {
            let receipt = $("#receipts-table").bootstrapTable("getSelections")[0];
            let selectedUser = $(event.target).val();
            let url = `http://localhost:5000/internal/${userid}/receipts/${receipt.id}/user/${selectedUser}`
            $.post(url, function(data) {
                console.log(data);
            });
        });
    });
}

function viewReceipt(event) {
    // if the select is clicked, don't view the receipt
    if ($(event.target).is("select")) {
        return;
    }
    let receipt = $("#receipts-table").bootstrapTable("getSelections")[0]
    $("#receipt-content-table").bootstrapTable("showLoading");
    if (receipt == null) {
        $("#receipt-content-table").bootstrapTable("hideLoading");
        $("#receipt-content-table").bootstrapTable("load", []); // clear table
    }
    let url = `http://localhost:5000/internal/${userid}/receipts/${receipt.id}`
    $.get(url, function(data) {
        $("#receipt-content-table").bootstrapTable("hideLoading");
        $("#receipt-content-table").bootstrapTable("load", data);
        // create selection event listeners
        $("#receipt-content-table > tbody > tr > td > select").change(function(event) {
            let receipt = $("#receipts-table").bootstrapTable("getSelections")[0];
            let selectedUser = $(event.target).val();
            let url = `http://localhost:5000/internal/${userid}/receipts/${receipt.id}/user/${selectedUser}`
            $.post(url, function(data) {
                console.log(data);
            }
            );
        });
    });
}

function dateFormatter(value, row) {
    return new Date(value).toLocaleString();
}

function priceFormatter(value, row) {
    if (row.currency == null)
        return value + " " + $("#receipts-table").bootstrapTable("getSelections")[0].currency;
    else
        return  value + " " + row.currency;
}
    
function associatedUsersFormatter(value, row) {
    // Create a selection box with all the group users and select the row.userId
    let select = $("<select></select>");
    for (let i = 0; i < groupUsers.length; i++) {
        let user = groupUsers[i];
        let option = $("<option></option>");
        option.attr("value", user.id);
        option.text(user.userName);
        if (user.id == row.userId)
            option.attr("selected", "selected");
        select.append(option);
    }
    return select.prop("outerHTML");
}

function associatedGroupsFormatter(value, row) {
    // Create a selection box with all the groups and select the row.groupId
    let select = $("<select></select>");
    for (let i = 0; i < groups.length; i++) {
        let group = groups[i];
        let option = $("<option></option>");
        option.attr("value", group.id);
        option.text(group.groupName);
        if (group.id == row.groupId)
            option.attr("selected", "selected");
        select.append(option);
    }
    return select.prop("outerHTML");
}


async function populateGroupUsers() {
    let url = `http://localhost:5000/internal/${userid}/groupMembers`
    await $.get(url, function(data) {
        groupUsers = data;
    });
}

async function populateGroups() {
    let url = `http://localhost:5000/internal/${userid}/groups`
    await $.get(url, function(data) {
        groups = data;
    });
}

$(document).ready(init);