'''
@author ldc

'''
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from MySites.settings import LOGIN_VISIT

'''
所有的钩子函数都可以返回一个Response
一旦钩子函数返回了Response,整个请求的受理就结束了
'''
# 继承于框架中间件
class SitesAppMiddleware(MiddlewareMixin):
	# 下钩子于所有路由被交给路由表之前
	def process_request(self,request):
		# 用户的请求是否需要在登录状态下才能查看
		if request.META.get('PATH_INFO',None) in LOGIN_VISIT:
			utoken = request.COOKIES.get('utoken', None)
			if not utoken:
				return redirect(reverse('SitesApp:login'))

	# 下钩子于所有路由请求被交给视图函数之前
	def process_view(self, request, view_func, view_args, view_kwargs):
		# print(">>>>>>>>>> process_view", request, view_func, view_args, view_kwargs)
		pass

	# 理论上下钩子于所有路由请求的模板被渲染完成以后
	# 这个函数实测无法回调
	def process_template_response(self, request, response):
		# print(">>>>>>>>>> process_template_response", request, response)
		return response

	# 下钩子于所有路由的响应被返回之前
	def process_response(self, request, response):
		# print(">>>>>>>>>> process_response", request, response)
		return response

	# def process_exception(self, request, exception):
	# 	print(">>>>>>>>>> process_exception", request, exception)
	# 	return redirect('/')