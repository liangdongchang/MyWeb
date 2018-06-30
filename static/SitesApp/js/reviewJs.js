tinyMCE.init({
    'mode': 'textareas',
    'theme': 'advanced',
    'width': 800,
    'height': 300,
    'language': 'zh',
    'style_formats': [
        {'title': 'Bold text', 'inline': 'b'},
        {'title': 'Red text', 'inline': 'span', 'styles': {'color': '#ff0000'}},
        {'title': 'Red header', 'block': 'h1', 'styles': {'color': '#ff0000'}},
        {'title': 'Example 1', 'inline': 'span', 'classes': 'example1'},
        {'title': 'Example 2', 'inline': 'span', 'classes': 'example2'},
        {'title': 'Table styles'},
        {'title': 'Table row 1', 'selector': 'tr', 'classes': 'tablerow1'}
    ]

});

var modal, id, url, type, rImpo, remark;
$('#exampleModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // 触发事件的按钮
    var topic = button.data('topic'); // 解析出data-topic内容
    var content = button.data('body'); // 解析出data-body内容
    type = button.data('type'); // 解析出data-type内容
    id = button.data('id'); // 解析出data-id内容
    url = button.data('url'); // 解析出data-url内容
    rImpo = button.data('rimpo'); // 解析出data-rImpo内容
    remark = button.data('remark'); // 解析出data-remark内容
    //如果是已办事项或归档事项，富文本框就不可编辑

    if (remark == 0 || remark == 3) {
        $('.btn-primary').css('display', 'none');
        $('#topic').attr('disabled', 'disabled');
        $('#rImpoSelect').attr('disabled', 'disabled');
        //设置富文本框不可编辑
        tinymce.activeEditor.getBody().setAttribute('contenteditable', false);
    } else {
        $('.btn-primary').css('display', 'inline-block');
        $('#topic').removeAttr("disabled");
        $('#rImpoSelect').removeAttr("disabled");
        tinymce.activeEditor.getBody().setAttribute('contenteditable', true);
    }
    modal = $(this);

    // alert(remark);
    if (type == 'add') {
        modal.find('#topic').attr('placeholder', '请填写事项主题');
        modal.find('.modal-title').text('');
        modal.find('#rImpoSelect').val(0);
        modal.find('#topic').val('');
        SetTinyMceContent('message-text', '');

    } else if (type == 'modify') {
        modal.find('.modal-title').text(topic);
        modal.find('#rImpoSelect').val(rImpo);
        modal.find('#topic').val(topic);
        SetTinyMceContent('message-text', content);
    }


});

$('.btn-primary').click(function () {
    // alert(123456);
    var content = tinyMCE.getInstanceById('message-text').getBody().innerHTML;
    var topic = modal.find('#topic').val();
    rImpo = modal.find('#rImpoSelect').val();
    if (topic.length == 0 || content.length == 0) {
        alert("事项主题和内容不能为空");
        return
    }
    $.ajax({
        type: "POST",
        url: url,
        data: {"id": id, "topic": topic, "content": content, "impo": rImpo, "remark": remark},
        dataType: "json",
        success: function (res) {
            // alert(res['ret']);
            $('#exampleModal').modal('hide');
            window.location.href = url;
        }
    });
});

// {       表单提交后，处理服务器返回的数据
$(document).ready(function () {
    $("#formAdd").ajaxForm(function (data) {
        // data = $.parseJSON(data);
        alert(tinyMCE.getInstanceById('message-text').getBody().innerHTML);
        alert(data['ret']);
    });
});

//editorId是富文本的id
function SetTinyMceContent(editorId, content) {
    //给富文本编辑器设置内容
    tinyMCE.getInstanceById(editorId).getBody().innerHTML = content;
    // tinyMCE.getInstanceById(editorId).getBody().val(content)  ;
    //获取富文本编辑器的内容
// alert(tinyMCE.getInstanceById(editorId).getBody().innerHTML);
}

