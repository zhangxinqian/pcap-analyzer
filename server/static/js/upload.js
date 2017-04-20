$(document).ready(function() {
    $('select.dropdown').dropdown();
    $('#upload-nav').addClass('active');
    $('.ui.checkbox').checkbox();

    //Select City
    var s={"Shanghai":[121,31],"Nanjing":[118,32]};
    function cityToStr(text){
        var arry_ll=s[text].toString().split(',');
        $("#cityMessage").html("City:"+text+", longitude="+arry_ll[0]+", latitude="+arry_ll[1]);
    }
    var text=$("#searchCity").find("option:selected").text();
        cityToStr(text);
    $("#searchCity").change(function(){
        text=$("#searchCity").find("option:selected").text();
        cityToStr(text);
    });

    //Select Type
    function typeToStr(text){
        $("#typeMessage").html("Type:"+text);
    }
    var type_text=$("#searchType").find("option:selected").text();
    typeToStr(type_text);
    $("#searchType").change(function(){
        type_text=$("#searchType").find("option:selected").text();
        typeToStr(type_text);
    });

//    //Contact
//    function contactToStr(text) {
//        $("#contactMessage").html("Device Info: "+text);
//    }
//    var contact_text=$("#searchContact").find("option:selected").text();
//    contactToStr(contact_text);
//    $("#searchContact").change(function(){
//        contact_text=$("#searchContact").find("option:selected").text();
//        $.post('/showContact', {
//            user_name : contact_text
//        }, function(data, status) {
//            alert(data);
//        });
//    });

    $('#delete-button').on('click', function(){
        $('.small.del.modal').modal({
            closable  : true,
            allowMultiple: false,
            onDeny    : function(){
                return true;
            },
            onApprove : function() {
                var delCheckbox = $("input[name='checkoption']:checked");
                var size = delCheckbox.size();
                if(size > 0){  
                    var params = "";  
                    for(var i=0;i<size;i++){
                        params+=delCheckbox.eq(i).val();
                        if (i != size-1){params=params+','};
                        }
                    $.post("delete/"+params,'',function(d){  
                            history.go(0);
                        },'text');
                    } 
            }
        }).modal('show');
    });

    $('#download-button').on('click', function(){
        var delCheckbox = $("input[name='checkoption']:checked");
        var size = delCheckbox.size();
        if(size > 0){  
            for(var i=0;i<size;i++){
                param=delCheckbox.eq(i).val();
                window.open('/download/'+param);
                }
        }
    });

    $('#analyze-button').on('click', function(){
        var delCheckbox = $("input[name='checkoption']:checked");
        var size = delCheckbox.size();
        var arry_ll=s[text].toString().split(',');
        if(size > 0){  
            for(var i=0;i<size;i++){
                param=delCheckbox.eq(i).val();
                window.open('/analyze/'+param+'?longitude='+arry_ll[0]+'&latitude='+arry_ll[1]+'&type='+type_text);
                }
        }
    });
     $('#send_gen_2').on('click', function(){
        var delCheckbox = $("input[name='checkoption']:checked");
        var size = delCheckbox.size();
        var arry_ll=s[text].toString().split(',');
        if(size > 0){
            for(var i=0;i<size;i++){
                param=delCheckbox.eq(i).val();
                window.open('/autogen_2/'+param+'?type='+type_text);
                }
        }
        });


    $('#fileupload').fileupload({
        url: '/upload',
        add: function (e, data) {
            var goUpload = true;
            var uploadFile = data.files[0];
            if (!(/\.(pcap)$/i).test(uploadFile.name)) {
                alert('Pcap file only!');
                goUpload = false;
            }
            if (uploadFile.size > 30000000) { // 2mb
                alert('Max Size is 30 MB!');
                goUpload = false;
            }
            if (goUpload == true) {
                data.submit();
            }
        },
        progressall: function (e, data) {
            $('.progress').progress({percent:1});
            var progressbar = parseInt(data.loaded / data.total * 100, 10);
            console.log(progressbar);
            $('.progress').progress({percent:progressbar});
        },
        done: function (e, data) {
            if (data['textStatus']=="success")
                $("#progresslabel").append("Upload OK!");
                $('#fileupload').attr({"disabled":"disabled"});
                $('.small.ok.modal').modal('show');

        },
    });

//    //Device
//    function deviceToStr(text) {
//        $("#deviceMessage").html("Device Info: "+text);
//    }
//    var device_text=$("#searchDevice").find("option:selected").text();
//    deviceToStr(device_text);
//    $("#searchDevice").change(function(){
//        device_text=$("#searchDevice").find("option:selected").text();
//        deviceToStr(device_text);
//    });

    $('input[name="device_id"]').blur(function() {
        var div1=document.getElementById('error_id');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_id").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_id").removeClass('error');
            div1.style.display='none';
        }
    });
    $('input[name="device_name"]').blur(function() {
        var div1=document.getElementById('error_name');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_name").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_name").removeClass('error');
            div1.style.display='none';
        }
    });
    $('input[name="device_imei"]').blur(function() {
        var div1=document.getElementById('error_imei');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_imei").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_imei").removeClass('error');
            div1.style.display='none';
        }
    });
    $('input[name="device_os"]').blur(function() {
        var div1=document.getElementById('error_os');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_os").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_os").removeClass('error');
            div1.style.display='none';
        }
    });
    $('input[name="device_serialNumber"]').blur(function() {
        var div1=document.getElementById('error_serialNumber');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_serialNumber").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_serialNumber").removeClass('error');
            div1.style.display='none';
        }
    });

   //Add Device Information
   $('#addDevice-button').on('click', function(){
       $('#addDevice-ok').modal({
            closable  : true,
            allowMultiple: false,
            onDeny    : function(){
                return true;
            },
            onApprove : function() {
                addDevice();
            }
        }).modal('show');
    });

    function addDevice() {
        var id_reg = /[A-F\d]{2}:[A-F\d]{2}:[A-F\d]{2}:[A-F\d]{2}:[A-F\d]{2}:[A-F\d]{2}/;

        var device_id = $('input[name="device_id"]').val();
        var device_name = $('input[name="device_name"]').val();
        var device_imei = $('input[name="device_imei"]').val();
        var device_os = $('input[name="device_os"]').val();
        var device_serialNumber = $('input[name="device_serialNumber"]').val();

        $.post('/addDevice', {
            device_id : device_id,
            device_name:device_name,
            device_imei: device_imei,
            device_os:device_os,
            device_serialNumber:device_serialNumber
        }, function(data) {
            if(data=='ok')
                window.location.reload();
        });
    }



   //Add Contact Information
   $('#addUser-button').on('click', function(){
       $('#addUser-ok').modal({
            closable  : true,
            allowMultiple: false,
            onDeny    : function(){
                return true;
            },
            onApprove : function() {
                addContact();
            }
        }).modal('show');
    });

    $('input[name="user_name"]').blur(function() {
        var div1=document.getElementById('error_user_name');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_user_name").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_user_name").removeClass('error');
            div1.style.display='none';
        }
    });

    $('input[name="user_companyName"]').blur(function() {
        var div1=document.getElementById('error_user_companyName');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_user_companyName").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_user_companyName").removeClass('error');
            div1.style.display='none';
        }
    });

    $('input[name="user_title"]').blur(function() {
        var div1=document.getElementById('error_user_title');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_user_title").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_user_title").removeClass('error');
            div1.style.display='none';
        }
    });

    $('input[name="user_mobile"]').blur(function() {
        var div1=document.getElementById('error_user_mobile');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_user_mobile").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_user_mobile").removeClass('error');
            div1.style.display='none';
        }
    });

    $('input[name="user_email"]').blur(function() {
        var div1=document.getElementById('error_user_email');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_user_email").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_user_email").removeClass('error');
            div1.style.display='none';
        }
    });

    $('input[name="user_groupName"]').blur(function() {
        var div1=document.getElementById('error_user_groupName');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_user_groupName").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_user_groupName").removeClass('error');
            div1.style.display='none';
        }
    });

    $('input[name="user_address"]').blur(function() {
        var div1=document.getElementById('error_user_address');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_user_address").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_user_address").removeClass('error');
            div1.style.display='none';
        }
    });

    $('input[name="user_nickname"]').blur(function() {
        var div1=document.getElementById('error_user_nickname');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_user_nickname").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_user_nickname").removeClass('error');
            div1.style.display='none';
        }
    });

    $('input[name="user_birthday"]').blur(function() {
        var div1=document.getElementById('error_user_birthday');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_user_birthday").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_user_birthday").removeClass('error');
            div1.style.display='none';
        }
    });

    $('input[name="user_notes"]').blur(function() {
        var div1=document.getElementById('error_user_birthday');
        if($(this).val() === "" || $(this).val() === null ) {
            $("#field_user_notes").addClass('error');
            div1.style.display='block';
        }
        else{
            $("#field_user_notes").removeClass('error');
            div1.style.display='none';
        }
    });

    function addContact() {
        var id_reg = /[A-F\d]{2}:[A-F\d]{2}:[A-F\d]{2}:[A-F\d]{2}:[A-F\d]{2}:[A-F\d]{2}/;

        var user_name = $('input[name="user_name"]').val();
        var user_companyName = $('input[name="user_companyName"]').val();
        var user_title = $('input[name="user_title"]').val();
        var user_mobile = $('input[name="user_mobile"]').val();
        var user_email = $('input[name="user_email"]').val();
        var user_groupName = $('input[name="user_groupName"]').val();
        var user_address = $('input[name="user_address"]').val();
        var user_nickname = $('input[name="user_nickname"]').val();
        var user_birthday = $('input[name="user_birthday"]').val();
        var user_notes = $('input[name="user_notes"]').val();

        $.post('/addContact', {
            user_name : user_name,
            user_companyName:user_companyName,
            user_title: user_title,
            user_mobile:user_mobile,
            user_email:user_email,
            user_groupName : user_groupName,
            user_address:user_address,
            user_nickname: user_nickname,
            user_birthday:user_birthday,
            user_notes:user_notes
        }, function(data) {
            if(data=='ok')
                window.location.reload();
        });
    }
});
