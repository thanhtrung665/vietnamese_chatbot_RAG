import json
import os
import glob

def merge_json_files(input_folder, output_file):
    """
    Tự động tìm và gộp tất cả các file .json trong một thư mục thành một file duy nhất.

    Args:
        input_folder (str): Đường dẫn đến thư mục chứa các file JSON đầu vào.
        output_file (str): Đường dẫn đến file JSON đầu ra sau khi đã gộp.
    """
    
    # Khởi tạo một danh sách rỗng để chứa toàn bộ dữ liệu gộp lại
    merged_data = []
    
    # Tạo đường dẫn tìm kiếm tất cả các file có đuôi .json trong thư mục đầu vào
    # Ví dụ: 'input_data/*.json'
    search_path = os.path.join(input_folder, '*.json')
    
    # Dùng glob để lấy danh sách tất cả các file phù hợp
    json_files = glob.glob(search_path)
    
    if not json_files:
        print(f"Không tìm thấy file JSON nào trong thư mục: {input_folder}")
        return

    print(f"Tìm thấy {len(json_files)} file JSON. Bắt đầu gộp...")

    # Duyệt qua từng file JSON tìm được
    for file_path in json_files:
        try:
            # Mở và đọc nội dung của file JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                # Dùng json.load() để chuyển đổi nội dung JSON thành đối tượng Python
                content = json.load(f)
                
                # Kiểm tra xem nội dung có phải là một danh sách không
                if isinstance(content, list):
                    # Nếu là danh sách, dùng extend để nối vào danh sách chính
                    merged_data.extend(content)
                else:
                    # Nếu không phải danh sách (ví dụ: một đối tượng duy nhất),
                    # thì thêm nó như một phần tử vào danh sách chính
                    merged_data.append(content)
            
            print(f" -> Đã đọc và xử lý thành công file: {os.path.basename(file_path)}")

        except json.JSONDecodeError:
            print(f"Lỗi: File '{os.path.basename(file_path)}' không phải là định dạng JSON hợp lệ.")
        except Exception as e:
            print(f"Lỗi không xác định khi xử lý file '{os.path.basename(file_path)}': {e}")
            
    # Sau khi đã đọc hết các file, ghi danh sách đã gộp vào file đầu ra
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # Dùng json.dump() để ghi đối tượng Python vào file JSON
            # indent=4: Giúp file JSON đầu ra được định dạng đẹp, dễ đọc
            # ensure_ascii=False: Đảm bảo các ký tự Unicode (như tiếng Việt) được ghi đúng
            json.dump(merged_data, f, indent=4, ensure_ascii=False)
        
        print("\n----------------------------------------------------")
        print(f"✅ Gộp file thành công!")
        print(f"Tổng cộng {len(merged_data)} đối tượng đã được ghi vào file: {output_file}")
        print("----------------------------------------------------")

    except Exception as e:
        print(f"\nLỗi khi ghi file đầu ra: {e}")


# --- CẤU HÌNH VÀ CHẠY SCRIPT ---
if __name__ == "__main__":
    # Tên thư mục chứa các file JSON cần gộp
    thu_muc_dau_vao = 'chatbot/Data_json'
    
    # Tên file JSON đầu ra sau khi gộp
    tep_dau_ra = 'merged_output.json'
    
    # Gọi hàm để thực hiện việc gộp file
    merge_json_files(thu_muc_dau_vao, tep_dau_ra)