from rest_framework import generics, permissions
from rest_framework.permissions import BasePermission

class ReviewCreatePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'client'

class OrdersPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'client'

class CourierPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'courier'



class StoreCreatePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'owner'