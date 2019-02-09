from django.shortcuts import render, HttpResponse, redirect
from utils import sqlhelper
from django.forms import Form
from django.forms import fields
from django.forms import widgets
import json


def has_auth(func):
    def auth(request, *args, **kwargs):
        try:
            request.get_signed_cookie('uname', salt='123456')
        except Exception:
            return redirect('stu:login')
        return func(request, *args, **kwargs)
    return auth


def logout(request):
    # request.session.delete(request.session.session_key)
    response = redirect('stu:login')
    response.delete_cookie('uname')
    return response


@has_auth
def classes(request):
    obj = sqlhelper.SqlHelper()
    class_list = obj.get_list("select id,title from class", [])
    obj.close()
    class_list = {
        'class_list': class_list
    }
    return render(request, 'classes.html', class_list)


def add_class(request):
    if request.method == 'GET':
        return render(request, 'add_class.html')
    else:
        c_name = request.POST.get('c_name')
        if len(c_name) > 0:
            obj = sqlhelper.SqlHelper()
            obj.modify("insert into class(title) values(%s)", [c_name, ])
            obj.close()
            return redirect('stu:classes')
        else:
            return render(request, 'add_class.html', {'msg': '班级名称不能为空'})


def del_class(request):
    c_id = request.GET.get('pk')
    try:
        sqlhelper.modify("delete from class where id=%s", [c_id, ])
        return redirect('stu:classes')
    except Exception as e:
        return HttpResponse('班级有学生不能删除')


def edit_class(request):
    if request.method == 'GET':
        c_id = request.GET.get('pk')
        obj = sqlhelper.SqlHelper()
        result = obj.get_one("select id,title from class where id=%s", [c_id, ])
        obj.close()
        return render(request, 'edit_class.html', result)
    else:
        c_id = request.GET.get('pk')
        edit_name = request.POST.get('edit_name')
        obj = sqlhelper.SqlHelper()
        obj.modify("update class set title=%s where id=%s", [edit_name, c_id, ])
        obj.close()
        return redirect('stu:classes')


@has_auth
def students(request):
    stu_list = sqlhelper.get_list(
        "select students.id,students.name,students.cid,class.id, class.title from students left join class on students.cid = class.id",
        [])
    class_list = sqlhelper.get_list("select * from class", [])
    return render(request, 'students.html', {'stu_list': stu_list, 'class_list': class_list})


def add_students(request):
    if request.method == 'GET':
        obj = sqlhelper.SqlHelper()
        class_list = obj.get_list("select id,title from class", [])
        obj.close()
        return render(request, 'add_students.html', {'class_list': class_list})
    else:
        s_name = request.POST.get('s_name')
        c_id = request.POST.get('c_id')
        obj = sqlhelper.SqlHelper()
        obj.modify("insert into students(name,cid) values(%s,%s)", [s_name, c_id])
        obj.close()
        return redirect('stu:students')


def del_students(request):
    s_id = request.GET.get('pk')
    obj = sqlhelper.SqlHelper()
    obj.modify("delete from students where id=%s", [s_id, ])
    obj.close()
    return redirect('stu:students')


def edit_students(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')
        class_list = sqlhelper.get_list("select id,title from class", [])
        current_stuinfo = sqlhelper.get_one("select id,name,cid from students where id=%s", [pk, ])
        return render(request, 'edit_students.html', {'class_list': class_list, 'current_stuinfo': current_stuinfo})
    else:
        pk = request.GET.get('pk')
        edit_name = request.POST.get('edit_name')
        c_id = request.POST.get('c_id')
        sqlhelper.modify("update students set name=%s,cid=%s where id=%s", [edit_name, c_id, pk])
        return redirect('stu:students')


################### 对话框  #####################
def modal_add_class(request):
    title = request.POST.get('title')
    if len(title) > 0:
        sqlhelper.modify('insert into class(title) values(%s)', [title, ])
        return HttpResponse('OK')
    else:
        # 页面不刷新，提示错误信息。
        return HttpResponse('标题不能为空')


def modal_edit_class(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        content = request.POST.get('content')
        sqlhelper.modify('update class set title=%s where id=%s', [content, nid])
    except Exception as e:
        ret['status'] = False
        ret['message'] = "处理异常"
    return HttpResponse(json.dumps(ret))


def modal_add_stu(request):
    s_name = request.POST.get('s_name')
    c_id = request.POST.get('c_id')
    if len(s_name) > 0:
        sqlhelper.modify("insert into students(name,cid) values(%s,%s)", [s_name, c_id])
        return HttpResponse('OK')
    else:
        return HttpResponse('姓名不能为空')


def modal_edit_stu(request):
    ret = {'status': True, 'message': None}
    edit_s_id = request.POST.get('edit_s_id')
    edit_s_name = request.POST.get('edit_s_name')
    edit_c_id = request.POST.get('edit_c_id')
    if len(edit_s_name) > 0:
        try:
            sqlhelper.modify("update students set name=%s, cid=%s where id=%s", [edit_s_name, edit_c_id, edit_s_id])
            return HttpResponse(json.dumps(ret))
        except Exception as e:
            ret['status'] = False
            ret['message'] = '处理异常'
            return HttpResponse(json.dumps(ret))
    else:
        ret['status'] = False
        ret['message'] = '姓名不能为空'
        return HttpResponse(json.dumps(ret))


# 多对多
@has_auth
def teachers(request):
    teacher_list = sqlhelper.get_list("""
    select teachers.id as tid, teachers.name, class.title from teachers
    left join relations on teachers.id = relations.t_id
    left join class on class.id = relations.c_id;
    """, [])
    result = {}
    for row in teacher_list:
        tid = row['tid']
        if tid in result:
            result[tid]['titles'].append(row['title'])
        else:
            result[tid] = {'tid': row['tid'], 'name': row['name'], 'titles': [row['title'], ]}
    return render(request, 'teachers.html', {'teacher_list': result.values()})


def add_teacher(request):
    if request.method == 'GET':
        class_list = sqlhelper.get_list("select id,title from class", [])
        return render(request, 'add_teacher.html', {'class_list': class_list})
    else:
        name = request.POST.get('name')
        teacher_id = sqlhelper.create("insert into teachers(name) value (%s)", [name, ])
        class_ids = request.POST.getlist('class_ids')
        data_list = []
        for cls_id in class_ids:
            temp = (teacher_id, cls_id,)
            data_list.append(temp)
        obj = sqlhelper.SqlHelper()
        obj.multiple_modify('insert into relations(t_id, c_id) values(%s, %s)', data_list)
        obj.close()
        return redirect('stu:teachers')


def edit_teacher(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        obj = sqlhelper.SqlHelper()
        teacher_info = obj.get_one('select id,name from teachers where id=%s', [nid, ])
        class_id_list = obj.get_list('select c_id from relations where t_id=%s', [nid, ])
        class_list = obj.get_list("select id,title from class", [])
        obj.close()
        temp = []
        for i in class_id_list:
            temp.append(i['c_id'])
        return render(request, 'edit_teacher.html', {
            'teacher_info': teacher_info,
            'class_id_list': temp,
            'class_list': class_list,
        })
    else:
        nid = request.GET.get('nid')
        name = request.POST.get('name')
        class_ids = request.POST.getlist('class_ids')
        obj = sqlhelper.SqlHelper()
        obj.modify('update teachers set name=%s where id=%s', [name, nid])
        obj.modify('delete from relations where t_id=%s', [nid, ])
        data_list = []
        for cls_id in class_ids:
            temp = (nid, cls_id,)
            data_list.append(temp)
        obj = sqlhelper.SqlHelper()
        obj.multiple_modify('insert into relations(t_id, c_id) values(%s, %s)', data_list)
        obj.close()
        return redirect('stu:teachers')


def get_all_class(request):
    obj = sqlhelper.SqlHelper()
    class_list = obj.get_list("select id,title from class", [])
    obj.close()
    return HttpResponse(json.dumps(class_list))


def modal_add_teacher(request):
    ret = {'status': True, 'message': None}
    try:
        name = request.POST.get('name')
        class_id_list = request.POST.getlist('class_id_list')
        teacher_id = sqlhelper.create("insert into teachers(name) value (%s)", [name, ])
        data_list = []
        for cls_id in class_id_list:
            temp = (teacher_id, cls_id,)
            data_list.append(temp)
        obj = sqlhelper.SqlHelper()
        obj.multiple_modify('insert into relations(t_id, c_id) values(%s, %s)', data_list)
        obj.close()
    except Exception as e:
        ret['status'] = False
        ret['message'] = "处理失败"
    return HttpResponse(json.dumps(ret))


def del_teacher(request):
    t_id = request.GET.get('t_id')
    sqlhelper.modify("delete from teachers where id=%s", [t_id, ])
    sqlhelper.modify("delete from relations where t_id=%s", [t_id, ])
    return redirect('stu:teachers')


def modal_edit_teacher(request):
    ret = {'status': True, 'message': None}
    try:
        name = request.POST.get('name')
        class_id_list = request.POST.getlist('class_id_list')
        t_id = request.POST.get('t_id')
        obj = sqlhelper.SqlHelper()
        obj.modify('update teachers set name=%s where id=%s', [name, t_id])
        obj.modify('delete from relations where t_id=%s', [t_id, ])
        data_list = []
        for cls_id in class_id_list:
            temp = (t_id, cls_id,)
            data_list.append(temp)
        obj = sqlhelper.SqlHelper()
        obj.multiple_modify('insert into relations(t_id, c_id) values(%s, %s)', data_list)
        obj.close()
    except Exception as e:
        ret['status'] = False
        ret['message'] = "处理失败"
    return HttpResponse(json.dumps(ret))


class LoginForm(Form):
    uname = fields.CharField(
        widget=widgets.TextInput(attrs={'style': 'width: 150px;float: left;margin-left: 20px', 'placeholder': '账号'}),
        max_length=18,
        min_length=2,
        required=True,
        label='用户名',
        error_messages={
            'required': '用户名为空',
            'min_length': '输入字符太短',
            'max_length': '输入字符太长'
        }
    )
    pwd = fields.CharField(
        widget=widgets.TextInput(attrs={'style': 'width: 150px;float: left;margin-left: 20px', 'placeholder': '密码'}),
        max_length=18,
        min_length=2,
        required=True,
        error_messages={
            'required': '密码为空',
            'min_length': '输入字符太短',
            'max_length': '输入字符太长'
        }
    )


def login(request):
    if request.method == 'GET':
        obj = LoginForm()
        return render(request, 'login.html', {'obj': obj})
    else:
        obj = LoginForm(request.POST)
        if obj.is_valid():
            uname = obj.cleaned_data['uname']
            pwd = obj.cleaned_data['pwd']
            result = sqlhelper.SqlHelper()
            userlogin = result.get_one("""
            select uname,pwd from ulogin where uname=%s and pwd=%s
            """, [uname, pwd, ])
            result.close()
            if userlogin:
                obj = redirect('stu:classes')
                obj.set_signed_cookie('uname', uname, salt='123456')
                return obj
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'obj': obj})
        else:
            return render(request, 'login.html', {'obj': obj})


class RegistForm(Form):
    uname = fields.CharField(
        widget=widgets.TextInput(attrs={'style': 'width: 150px;float: left;margin-left: 20px', 'placeholder': '账号'}),
        max_length=18,
        min_length=2,
        required=True,
        label='用户名',
        error_messages={
            'required': '用户名为空',
            'min_length': '输入字符太短',
            'max_length': '输入字符太长'
        }
    )
    pwd = fields.CharField(
        widget=widgets.TextInput(attrs={'style': 'width: 150px;float: left;margin-left: 20px', 'placeholder': '密码'}),
        max_length=18,
        min_length=2,
        required=True,
        label='密码',
        error_messages={
            'required': '密码为空',
            'min_length': '输入字符太短',
            'max_length': '输入字符太长'
        }
    )


def register(request):
    if request.method == 'GET':
        obj = RegistForm()
        return render(request, 'register.html', {'obj': obj})
    else:
        obj = LoginForm(request.POST)
        if obj.is_valid():
            uname = obj.cleaned_data['uname']
            pwd = obj.cleaned_data['pwd']
            result = sqlhelper.SqlHelper()
            result.modify("""
            insert into ulogin(uname,pwd) values(%s,%s)
            """, [uname, pwd])
            result.close()
            obj = redirect('stu:classes')
            obj.set_signed_cookie('uname', uname, salt='123456')
            return obj
        else:
            return render(request, 'register.html', {'obj': obj})

