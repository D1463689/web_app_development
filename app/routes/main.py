from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
# from app.models.models import Book # 暫時註解，實作時解除

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/books')
def index():
    """
    GET / 或 /books
    顯示所有書籍列表（首頁）
    """
    pass

@main_bp.route('/books/new', methods=['GET'])
def new_book():
    """
    GET /books/new
    顯示新增書籍的表單頁面
    """
    pass

@main_bp.route('/books', methods=['POST'])
def create_book():
    """
    POST /books
    接收表單資料，存入資料庫後重導向至首頁
    """
    pass

@main_bp.route('/books/<int:id>', methods=['GET'])
def book_detail(id):
    """
    GET /books/<id>
    顯示單筆書籍的詳情、心得與評分
    """
    pass

@main_bp.route('/books/<int:id>/edit', methods=['GET'])
def edit_book(id):
    """
    GET /books/<id>/edit
    顯示編輯書籍與心得的表單頁面
    """
    pass

@main_bp.route('/books/<int:id>/update', methods=['POST'])
def update_book(id):
    """
    POST /books/<id>/update
    接收編輯表單資料，更新資料庫後重導向至詳情頁
    """
    pass

@main_bp.route('/books/<int:id>/delete', methods=['POST'])
def delete_book(id):
    """
    POST /books/<id>/delete
    刪除指定書籍後重導向至首頁
    """
    pass
