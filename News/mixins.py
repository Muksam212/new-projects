#to give permission by creating groups
from django.core.exceptions import PermissionDenied

class GroupRequiredMixin(object):
	group_required=None

	def dispatch(self, request, *args, **kwargs):
		user_groups=[]

		for group in request.user.groups.values_list('name', flat=True):
			user_groups.append(group)

		print(self.group_required,"hello world")
		if len(set(user_groups).intersection(self.group_required)) <= 0:
			raise PermissionDenied

		return super().dispatch(request, *args, **kwargs)

