from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.models import Book

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/books')
def index():
    """
    GET / 或 /books
    顯示所有書籍列表（首頁）
    """
    books = Book.get_all()
    return render_template('index.html', books=books)

@main_bp.route('/books/new', methods=['GET'])
def new_book():
    """
    GET /books/new
    顯示新增書籍的表單頁面
    """
    return render_template('new_book.html')

@main_bp.route('/books', methods=['POST'])
def create_book():
    """
    POST /books
    接收表單資料，存入資料庫後重導向至首頁
    """
    title = request.form.get('title')
    author = request.form.get('author')
    category = request.form.get('category')
    
    if not title:
        flash('書名為必填欄位！', 'danger')
        return redirect(url_for('main.new_book'))
        
    try:
        Book.create(title=title, author=author, category=category)
        flash('書籍已成功新增！', 'success')
        return redirect(url_for('main.index'))
    except Exception as e:
        flash(f'新增書籍時發生錯誤：{str(e)}', 'danger')
        return redirect(url_for('main.new_book'))

@main_bp.route('/books/<int:id>', methods=['GET'])
def book_detail(id):
    """
    GET /books/<id>
    顯示單筆書籍的詳情、心得與評分
    """
    book = Book.get_by_id(id)
    if not book:
        abort(404)
    return render_template('detail.html', book=book)

@main_bp.route('/books/<int:id>/edit', methods=['GET'])
def edit_book(id):
    """
    GET /books/<id>/edit
    顯示編輯書籍與心得的表單頁面
    """
    book = Book.get_by_id(id)
    if not book:
        abort(404)
    return render_template('edit_book.html', book=book)

@main_bp.route('/books/<int:id>/update', methods=['POST'])
def update_book(id):
    """
    POST /books/<id>/update
    接收編輯表單資料，更新資料庫後重導向至詳情頁
    """
    book = Book.get_by_id(id)
    if not book:
        abort(404)
        
    title = request.form.get('title')
    author = request.form.get('author')
    category = request.form.get('category')
    status = request.form.get('status')
    rating = request.form.get('rating')
    notes = request.form.get('notes')
    
    if not title:
        flash('書名為必填欄位！', 'danger')
        return redirect(url_for('main.edit_book', id=id))
        
    try:
        # 處理 rating 型別轉換
        if rating and rating.isdigit():
            rating = int(rating)
        else:
            rating = None
            
        book.update(
            title=title, 
            author=author, 
            category=category, 
            status=status, 
            rating=rating, 
            notes=notes
        )
        flash('書籍資訊已成功更新！', 'success')
        return redirect(url_for('main.book_detail', id=id))
    except Exception as e:
        flash(f'更新書籍時發生錯誤：{str(e)}', 'danger')
        return redirect(url_for('main.edit_book', id=id))

@main_bp.route('/books/<int:id>/delete', methods=['POST'])
def delete_book(id):
    """
    POST /books/<id>/delete
    刪除指定書籍後重導向至首頁
    """
    book = Book.get_by_id(id)
    if not book:
        abort(404)
        
    try:
        book.delete()
        flash('書籍已成功刪除！', 'success')
    except Exception as e:
        flash(f'刪除書籍時發生錯誤：{str(e)}', 'danger')
        
    return redirect(url_for('main.index'))
