import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# --- 페이지 설정 ---
st.set_page_config(page_title="PRO부동산 매물제작기", page_icon="🏢")

# --- 폰트 로드 함수 (캐싱하여 속도 향상) ---
@st.cache_resource
def load_fonts():
    # 폰트 파일이 같은 폴더에 있어야 합니다. 없으면 기본 폰트로 대체될 수 있음.
    font_path = "malgunbd.ttf" 
    try:
        return font_path
    except:
        st.error("폰트 파일을 찾을 수 없습니다. 'malgunbd.ttf'를 같은 폴더에 넣어주세요.")
        return None

# --- 이미지 생성 함수 (기존 로직 유지) ---
def generate_image(data, font_path):
    # 1. 캔버스 생성
    width, height = 1300, 950
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 2. 색상 정의
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 20, 20)
    GRAY_BG = (240, 240, 240) 
    PINK_BG = (255, 230, 230) 

    # 3. 폰트 로드 (경로 문제 방지)
    try:
        f_header_title = ImageFont.truetype(font_path, 95)
        f_header_type = ImageFont.truetype(font_path, 100)
        f_brand = ImageFont.truetype(font_path, 35)
        f_invest_val = ImageFont.truetype(font_path, 115)
        f_invest_unit = ImageFont.truetype(font_path, 50)
        f_invest_label = ImageFont.truetype(font_path, 70)
        f_table_head = ImageFont.truetype(font_path, 35)
        f_table_val = ImageFont.truetype(font_path, 85)    
        f_table_unit = ImageFont.truetype(font_path, 35)   
        fonts_list_normal = [ImageFont.truetype(font_path, 38), ImageFont.truetype(font_path, 34), ImageFont.truetype(font_path, 26)]
        f_list_label_matched = ImageFont.truetype(font_path, 38) 
        f_right_sm = ImageFont.truetype(font_path, 23)     
        f_right_md = ImageFont.truetype(font_path, 35)     
        f_right_md_unit = ImageFont.truetype(font_path, 20)
        f_right_lg = ImageFont.truetype(font_path, 65)     
        f_right_contact = ImageFont.truetype(font_path, 35) 
        fonts_platform = [ImageFont.truetype(font_path, 21), ImageFont.truetype(font_path, 18)]
        f_footer = ImageFont.truetype(font_path, 35)
    except IOError:
        st.error("폰트 파일을 읽을 수 없습니다.")
        return None

    # --- 헬퍼 함수들 (내부 정의) ---
    def draw_val_unit(draw, x, y, value, font_val, font_unit, color, anchor="mm", unit_y_offset=0):
        unit_text = "억"
        w_val = draw.textlength(value, font=font_val)
        w_unit = draw.textlength(unit_text, font=font_unit)
        total_w = w_val + w_unit
        start_x = x - (total_w / 2)
        draw.text((start_x, y), value, fill=color, font=font_val, anchor="lm")
        draw.text((start_x + w_val, y + unit_y_offset), unit_text, fill=color, font=font_unit, anchor="lm")

    def draw_adaptive_text(draw, x, y, text, font_candidates, color, max_width, anchor="mm"):
        selected_font = font_candidates[-1]
        for font in font_candidates:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            if text_w <= max_width:
                selected_font = font
                break
        draw.text((x, y), text, fill=color, font=selected_font, anchor=anchor)

    # ================= [그리기 로직 시작] =================
    # (기존 코드와 100% 동일한 좌표/로직 사용)
    
    # [Section 1] Header
    header_h = 160 
    draw.rectangle([(0, 0), (width, header_h)], fill=BLACK)
    draw.multiline_text((40, header_h/2), "대한민국 부동산\nNO.1 플랫폼", fill=WHITE, font=f_brand, anchor="lm", align="center")
    draw.text((width/2 - 10, header_h/2), f"노량진 {data['dist_num']}구역", fill=WHITE, font=f_header_title, anchor="mm")
    draw.text((width/2 + 410, header_h/2), data['prop_type'], fill=YELLOW, font=f_header_type, anchor="mm")

    # [Section 2] Yellow Box
    invest_h = 170
    invest_y = header_h 
    draw.rectangle([(0, invest_y), (width, invest_y + invest_h)], fill=YELLOW)
    
    txt_label, txt_colon, txt_val, txt_unit = "초기투자금", ":", data['invest_price'], "억"
    gap_1, gap_2 = 30, 30
    w_label = draw.textlength(txt_label, font=f_invest_label)
    w_colon = draw.textlength(txt_colon, font=f_invest_label)
    w_val = draw.textlength(txt_val, font=f_invest_val)
    w_unit = draw.textlength(txt_unit, font=f_invest_unit)
    total_w = w_label + gap_1 + w_colon + gap_2 + w_val + w_unit
    start_x = (width - total_w) / 2 - 50 
    base_y = invest_y + invest_h/2
    cur_x = start_x
    draw.text((cur_x, base_y), txt_label, fill=RED, font=f_invest_label, anchor="lm")
    cur_x += w_label + gap_1
    draw.text((cur_x, base_y - 5), txt_colon, fill=RED, font=f_invest_label, anchor="lm")
    cur_x += w_colon + gap_2
    draw.text((cur_x, base_y - 8), txt_val, fill=RED, font=f_invest_val, anchor="lm")
    cur_x += w_val
    draw.text((cur_x, base_y + 8), txt_unit, fill=RED, font=f_invest_unit, anchor="lm")

    # [Section 3] Table
    table_y = invest_y + invest_h
    row_h_head, row_h_val = 70, 120   
    total_table_h = row_h_head + row_h_val
    col_w = width / 6
    draw.rectangle([(col_w * 4, table_y), (width, table_y + total_table_h)], fill=PINK_BG)
    draw.rectangle([(0, table_y), (col_w * 4, table_y + row_h_head)], fill=GRAY_BG)
    draw.line([(0, table_y + row_h_head), (width, table_y + row_h_head)], fill=BLACK, width=3)
    cols = ["매매가", "프리미엄", "권리가", "임대", "총 매수가", "안전마진"]
    vals = [data['p_sale'], data['p_premium'], data['p_rights'], data['p_rent'], data['p_total'], data['p_margin']]
    for i in range(6):
        x = i * col_w
        if i > 0: draw.line([(x, table_y), (x, table_y + total_table_h)], fill=BLACK, width=3)
        draw.text((x + col_w/2, table_y + row_h_head/2), cols[i], fill=BLACK, font=f_table_head, anchor="mm")
        val_center_y = table_y + row_h_head + (row_h_val / 2)
        val_str = vals[i].strip()
        c = RED if i == 1 else BLACK
        if val_str:
            draw_val_unit(draw, x + col_w/2, val_center_y, val_str, f_table_val, f_table_unit, c, "mm", unit_y_offset=12)
        else:
            draw.text((x + col_w/2, val_center_y), "-", fill=c, font=f_table_val, anchor="mm")
    
    # 테두리
    draw.line([(0, table_y), (width, table_y)], fill=BLACK, width=3)
    draw.line([(0, table_y + total_table_h), (width, table_y + total_table_h)], fill=BLACK, width=3)
    draw.line([(0, table_y), (0, table_y + total_table_h)], fill=BLACK, width=3)
    draw.line([(width, table_y), (width, table_y + total_table_h)], fill=BLACK, width=3)

    # [Section 4] Details
    detail_y = table_y + total_table_h
    footer_h = 70
    footer_y = height - footer_h
    detail_h = footer_y - detail_y 
    split_x = col_w * 4 
    list_items = [(data['list_1'], True), (data['list_2'], False), (data['list_3'], False), (data['list_4'], False), (data['list_5'], False)]
    line_gap = detail_h / 5 
    start_ly = detail_y + (line_gap / 2)
    left_padding, max_list_text_width = 20, split_x - 20 - 60 

    for i, (text, is_red) in enumerate(list_items):
        cur_y = start_ly + (i * line_gap)
        line_y = detail_y + ((i + 1) * line_gap)
        draw.line([(0, line_y), (split_x, line_y)], fill=BLACK, width=1)
        icon_size = 20
        draw.rectangle([(left_padding, cur_y - 10), (left_padding + icon_size, cur_y + 10)], outline=BLACK, width=3)
        draw.rectangle([(left_padding+4, cur_y - 6), (left_padding + icon_size-4, cur_y + 6)], fill=BLACK)
        color_use = RED if is_red else BLACK
        if i == 1 and ":" in text:
            parts = text.split(":", 1)
            label_part, desc_part = parts[0] + ":", parts[1]
            draw.text((left_padding + 40, cur_y), label_part, fill=color_use, font=f_list_label_matched, anchor="lm")
            label_w = draw.textlength(label_part, font=f_list_label_matched)
            remaining_w = max_list_text_width - label_w - 10
            desc_fonts = [ImageFont.truetype(font_path, 32), ImageFont.truetype(font_path, 28), ImageFont.truetype(font_path, 24)]
            draw_adaptive_text(draw, left_padding + 40 + label_w + 10, cur_y, desc_part, desc_fonts, color_use, remaining_w, anchor="lm")
        else:
            draw_adaptive_text(draw, left_padding + 40, cur_y, text, fonts_list_normal, color_use, max_list_text_width, anchor="lm")

    # Right Side
    draw.line([(split_x, detail_y), (split_x, detail_y + detail_h)], fill=BLACK, width=2)
    r_row1_h = 70 
    draw.line([(split_x, detail_y + r_row1_h), (width, detail_y + r_row1_h)], fill=BLACK, width=2)
    sub_split = split_x + 290 
    draw.line([(sub_split, detail_y), (sub_split, detail_y + r_row1_h)], fill=BLACK, width=2)
    label_center_x = split_x + (sub_split - split_x) / 2
    draw.text((label_center_x, detail_y + r_row1_h/2), "34평 예상 조합원 분양가", fill=BLACK, font=f_right_sm, anchor="mm")
    val_center_x = sub_split + (width-sub_split)/2
    draw_val_unit(draw, val_center_x, detail_y + r_row1_h/2, data['est_price'], f_right_md, f_right_md_unit, BLACK, "mm", unit_y_offset=2)
    
    r_row2_h = 160
    mid_y = detail_y + r_row1_h
    draw.line([(split_x, mid_y + r_row2_h), (width, mid_y + r_row2_h)], fill=BLACK, width=2)
    draw.text((split_x + (width-split_x)/2, mid_y + r_row2_h/2), data['comp_type'], fill=BLACK, font=f_right_lg, anchor="mm")
    
    bot_y_start = mid_y + r_row2_h
    remaining_h = detail_h - r_row1_h - r_row2_h
    draw.line([(split_x, bot_y_start + (remaining_h/2)), (width, bot_y_start + (remaining_h/2))], fill=BLACK, width=1)
    platform_area_w = width - split_x - 10
    draw_adaptive_text(draw, split_x + (width-split_x)/2, bot_y_start + (remaining_h/4), "대한민국 재개발 재건축 NO.1 플랫폼", fonts_platform, BLACK, platform_area_w, anchor="mm")
    draw.text((split_x + (width-split_x)/2, bot_y_start + (remaining_h * 0.75)), f"서프로 : {data['contact']}", fill=BLACK, font=f_right_contact, anchor="mm")

    # [Section 5] Footer
    draw.rectangle([(0, footer_y), (width, height)], fill=BLACK)
    t1, t2, t3 = f"노량진{data['dist_num']}구역 가장 최신 진행상황은 ", "아래▼ ", "자세히 나와있습니다."
    w1, w2, w3 = draw.textlength(t1, font=f_footer), draw.textlength(t2, font=f_footer), draw.textlength(t3, font=f_footer)
    start_fx = (width - (w1+w2+w3)) / 2
    draw.text((start_fx, footer_y + footer_h/2), t1, fill=WHITE, font=f_footer, anchor="lm")
    draw.text((start_fx + w1, footer_y + footer_h/2), t2, fill=RED, font=f_footer, anchor="lm")
    draw.text((start_fx + w1 + w2, footer_y + footer_h/2), t3, fill=WHITE, font=f_footer, anchor="lm")

    return image

# --- 메인 화면 구성 (스마트폰에 최적화) ---
st.title("PRO부동산 매물 카드 생성기")
st.write("모바일에서 입력하고 이미지를 다운로드하세요!")

font_path = load_fonts()

if font_path:
    with st.form("property_form"):
        st.subheader("1. 기본 정보")
        col1, col2 = st.columns(2)
        dist_num = col1.text_input("구역 번호", "1")
        prop_type = col2.text_input("매물 타입", "1+1")
        invest_price = st.text_input("초기투자금 (숫자만)", "18")

        st.subheader("2. 가격 테이블 (숫자만)")
        c1, c2, c3 = st.columns(3)
        p_sale = c1.text_input("매매가", "28")
        p_premium = c2.text_input("프리미엄", "17.8")
        p_rights = c3.text_input("권리가", "10.2")
        
        c4, c5, c6 = st.columns(3)
        p_rent = c4.text_input("임대", "10")
        p_total = c5.text_input("총 매수가", "36.8")
        p_margin = c6.text_input("안전마진", "16")

        st.subheader("3. 상세 정보")
        list_1 = st.text_input("상태 (빨강)", "대출불가")
        list_2 = st.text_input("조합원분양가 설명", "조합원분양가 : (34평 10.5억 , 24평 8.5억) = 분양가합 19억")
        list_3 = st.text_input("이주비", "이주비 최대 9억 지급예정")
        list_4 = st.text_input("시세 전망", "84기준 입주시 예상시세 MIN 30억 예상")
        list_5 = st.text_input("분담금 조건", "추가분담금은 입주 시, 90% 납부 예정")

        st.subheader("4. 우측 박스 & 연락처")
        est_price = st.text_input("34평 조합원분양가", "10.5")
        comp_type = st.text_input("구성 타입", "84㎡+59㎡")
        contact = st.text_input("연락처", "010.2319.0977")

        submitted = st.form_submit_button("📸 이미지 생성하기", use_container_width=True)

    if submitted:
        # 데이터 딕셔너리 생성
        data = {
            "dist_num": dist_num, "prop_type": prop_type, "invest_price": invest_price,
            "p_sale": p_sale, "p_premium": p_premium, "p_rights": p_rights,
            "p_rent": p_rent, "p_total": p_total, "p_margin": p_margin,
            "list_1": list_1, "list_2": list_2, "list_3": list_3, "list_4": list_4, "list_5": list_5,
            "est_price": est_price, "comp_type": comp_type, "contact": contact
        }

        # 이미지 생성
        result_img = generate_image(data, font_path)
        
        if result_img:
            st.image(result_img, caption="생성된 매물 카드", use_container_width=True)
            
            # 다운로드 버튼 (메모리 버퍼 사용)
            buf = io.BytesIO()
            result_img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            file_name = f"매물정보_노량진{dist_num}구역.png"
            st.download_button(
                label="💾 이미지 다운로드",
                data=byte_im,
                file_name=file_name,
                mime="image/png",
                use_container_width=True
            )
