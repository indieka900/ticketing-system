$(document).ready(function(){
	$('#employeeTable').Tabledit({
		deleteButton: false,
		editButton: false, 
		deleteButton: false,
    	autoFocus: false,
		columns: {
		  identifier: [0, 'UserId'],                    
		  editable: [[4, 'usertype', '{"Admin": "Admin", "Service Desk": "Service Desk", "IT Expert": "IT Expert", "Client": "Client"}'], [5, 'status','{"Yes": "Confirmed", "No": "Denied"}']]
		},
		hideIdentifier: true,
		url: 'save_edit.php',
		onSuccess: function(data, textStatus, jqXHR) {
                alert('Updated!');
            },
		
		onFail: function(jqXHR, textStatus, errorThrown) {
        console.log('onFail(jqXHR, textStatus, errorThrown)');
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
        },
        onAjax: function(action, serialize) {
                // open your xhr here 
                console.log("on Ajax");
                console.log("action : ", action);
                console.log("data : ", serialize);
            }			
	});

	$('#employeeTable1').Tabledit({
		hideIdentifier: true,
		url: 'save_edit.php',
		deleteButton: false,
		editButton: true,   		
		columns: {
		  identifier: [0, 'UserId'],                    
		  editable: [[1, 'name'], [2, 'usertype','{"Admin": "Admin", "Service Desk": "Service Desk", "IT Expert": "IT Expert", "Client": "Client"}'], [3, 'aos','{"Networking": "Networking", "Software": "Software", "Hardware": "Hardware"}']]
		},
		onSuccess: function(data, textStatus, jqXHR) {
                alert('Updated!');
            },
		
		onFail: function(jqXHR, textStatus, errorThrown) {
        console.log('onFail(jqXHR, textStatus, errorThrown)');
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
        },
        onAjax: function(action, serialize) {
                // open your xhr here 
                console.log("on Ajax");
                console.log("action : ", action);
                console.log("data : ", serialize);
            }		
	});

	$('#employeeTable2').Tabledit({
		deleteButton: true,
		editButton: false,   		
		columns: {
		  identifier: [0, 'UserId'],                    
		  editable: []
		},
		hideIdentifier: true,
		url: 'save_edit.php'
		
	});
});