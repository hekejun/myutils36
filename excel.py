# -*- coding: UTF-8 -*-
"""
File: excel.py
excel的接口，注意使用ExcelWrapper来作为读写接口，默认创建FullExcel，可以通过use_fast=True来创建FastExcel
"""
from __future__ import division

import win32com.client
import xlrd
import xlwt

import files
from check import check_func

__all__ = ["ExcelWrapper"]


class ExcelWrapper(object):
    """
    FullExcel依赖win32com包，该第三方包目前仅支持Windows平台使用，因此ExcelWrapper如果在Linux及其他平台使用，需注释FullExcel相关代码
    """

    def __init__(self, file_name, mode, sheet_name=None, use_fast=False):
        if use_fast:
            self.excel_helper = FastExcel(file_name, mode, sheet_name=sheet_name)
        else:
            self.excel_helper = FullExcel(file_name, mode, sheet_name=sheet_name)

    def __enter__(self):
        return self.excel_helper

    def __exit__(self, type, value, traceback):
        self.excel_helper.close()


class FullExcel(object):
    """
    基于win32com的Excel操作接口，特点是：打开速度较慢，但是功能丰富，可以做各种单元格操作，格式操作
    """

    @check_func(__file__, "FullExcel")
    def __init__(self, file_name, mode, sheet_name):
        self.excel = win32com.client.DispatchEx('Excel.Application')
        self.excel.visible = False
        self.file_name = file_name
        self.mode = mode
        if mode == "read":
            if file_name.find(":") == -1:
                # win32com只能基于Windows平台使用，所以可以用:符判断是否使用了绝对路径
                raise Exception("File should be an absoulte file path (d:\\xx.xlsx): %s" % file_name)
            if not files.has_file(file_name):
                raise Exception("File not exists: %s" % file_name)
            self.book = self.excel.Workbooks.Open(file_name)
        elif mode == "write":
            if not sheet_name:
                raise Exception("Full excel mode is write, need a sheet name.")
            self.book = self.excel.Workbooks.Add()
            self.book.Worksheets(1).Name = sheet_name
        else:
            pass

    @check_func(__file__, "FullExcel")
    def add_sheet(self, sheet_name):
        """
        根据sheet名新增一个sheet
        :param sheet_name: 输入的sheet名
        :return:
        """
        self.book.Worksheets.Add()
        self.book.Worksheets(1).Name = sheet_name
        return True

    @check_func(__file__, "FullExcel")
    def del_sheet(self, sheet_name):
        """
        根据sheet名删除excel
        :param sheet_name:
        :return: 删除成功True
        """
        self.excel.DisplayAlerts = False
        sht = self.get_sheet_like_name(sheet_name)
        if sht == 0:
            return False
        self.book.Worksheets(sht).Delete()
        self.excel.DisplayAlerts = True
        return True

    @check_func(__file__, "FullExcel")
    def set_sheet_visiable(self, name, status):
        """
        设置sheet表的访问状态
        :param name:
        :param status:
        :return:
        """
        self.excel.DisplayAlerts = False
        sht = self.get_sheet_by_name(name)
        if sht == 0:
            return False
        self.book.Worksheets(sht).Visible = status
        self.excel.DisplayAlerts = True
        return True

    @check_func(__file__, "FullExcel")
    def change_alert(self, status):
        """
        修改当前的文件的告警设置
        :param status:
        :return:
        """
        self.excel.DisplayAlerts = status

    @check_func(__file__, "FullExcel")
    def close(self):
        """
        保存后关闭excel对象，并回收内存
        :return:
        """

        self.change_alert(False)
        if self.mode == "write":
            self.book.SaveAs(self.file_name)
        else:
            self.book.Save()
        self.book.Close(SaveChanges=0)
        self.excel.Quit()
        self.change_alert(True)
        del self.excel
        return True

    @check_func(__file__, "FullExcel")
    def transfer_col_text(self, col_num):
        """
        将col的index值转换为表达值，例如第一列为A,第二列为B，仅支持两个字母的转换
        :param col_num:输入的column的index值
        :return:
        """
        if col_num > 702 or col_num < 1:
            return None
        if col_num < 27:
            s1 = chr(ord("A") + col_num - 1)
            str1 = str(s1)
        else:
            i = chr(ord("A") + (col_num - 1) / 26 - 1)
            j = chr(ord("A") + (col_num - ((col_num - 1) / 26) * 26) - 1)
            str1 = str(i) + "" + str(j)
        return str1

    @check_func(__file__, "FullExcel")
    def get_cell(self, sheet, row, col):
        """
        Get value of one cell
        :param sheet: sheet的index
        :param row: 第几行
        :param col: 第激烈
        :return: 返回单元格的值
        """
        sht = self.book.Worksheets(sheet)
        return sht.Cells(row, col).Value

    @check_func(__file__, "FullExcel")
    def set_cell(self, sheet, row, col, value):
        """
        设置某个单元格的值
        :param sheet:
        :param row:
        :param col:
        :param value:
        :return:
        """
        sht = self.book.Worksheets(sheet)
        sht.Cells(row, col).Value = value

    @check_func(__file__, "FullExcel")
    def get_comment(self, sheet, row, col):
        """
        获得某一个单元格的注解
        :param sheet:
        :param row:
        :param col:
        :return:
        """
        sht = self.book.Worksheets(sheet)
        cell_text = self.transfer_col_text(col) + str(row)
        sht.Range(cell_text).Comment.Visible = True
        return sht.Range(cell_text).Comment.Text()

    @check_func(__file__, "FullExcel")
    def get_sheets_size(self):
        """
        获得sheet数量
        :return:
        """
        return self.book.Worksheets.count

    @check_func(__file__, "FullExcel")
    def get_row_size(self, sheet, id):
        """
        获得某一行的数据最高值
        :param sheet:
        :param id:
        :return:
        """
        char = chr(ord('A') + id - 1)
        sht = self.book.Worksheets(sheet)
        col = str(char) + "65535"
        return sht.Range(col).End(-4162).Row

    @check_func(__file__, "FullExcel")
    def get_col_size(self, sheet, id):
        """
        获得某一列的数据最高值
        :param sheet:
        :return:
        """
        col_text = "IV" + str(id)
        sht = self.book.Worksheets(sheet)
        return sht.Range(col_text).End(-4159).Column

    @check_func(__file__, "FullExcel")
    def set_comment(self, sheet, row, col, data):
        """
        设置某个单元格的注释
        :param sheet:
        :param row:
        :param col:
        :param data:
        :return:
        """
        sht = self.book.Worksheets(sheet)
        sht.Cells(row, col).AddComment(data)

    @check_func(__file__, "FullExcel")
    def get_range(self, sheet, top_row, lef_col, buttom_row, right_col):
        """
        获得某个区域的数值
        :param sheet:
        :param top_row:
        :param lef_col:
        :param buttom_row:
        :param right_col:
        :return:
        """
        if top_row > buttom_row or lef_col > right_col:
            raise Exception("Input invalid-- [row %d-%d], [column %d-%d]" % (top_row, buttom_row, lef_col, right_col))
        sht = self.book.Worksheets(sheet)
        return sht.Range(sht.Cells(top_row, lef_col), sht.Cells(buttom_row, right_col)).Value

    @check_func(__file__, "FullExcel")
    def set_range(self, sheet, top_row, lef_col, buttom_row, right_col, data_list):
        """
        设置某个区域的数值
        :param sheet:
        :param top_row:
        :param lef_col:
        :param buttom_row:
        :param right_col:
        :param data_list:
        :return:
        """
        if data_list and (buttom_row - top_row + 1) != len(data_list) or (right_col - lef_col + 1) != len(data_list[0]):
            raise Exception("Data area not match [row %d-%d vs %d]--[column %d-%d vs %d] " % (
                top_row, buttom_row, len(data_list), lef_col, right_col, len(data_list[0])))
        sht = self.book.Worksheets(sheet)
        sht.Range(sht.Cells(top_row, lef_col), sht.Cells(buttom_row, right_col)).Value = data_list
        return True

    @check_func(__file__, "FullExcel")
    def merge_cell(self, sheet, top_row, lef_col, buttom_row, right_col, data):
        """
        合并指定区域的单元格，并设置值
        :param sheet:
        :param top_row:
        :param lef_col:
        :param buttom_row:
        :param right_col:
        :param data:
        :return:
        """
        if top_row > buttom_row or lef_col > right_col:
            raise Exception("Input invalid-- [row %d-%d], [column %d-%d]" % (top_row, buttom_row, lef_col, right_col))
        sht = self.book.Worksheets(sheet)
        sht.Range(sht.Cells(top_row, lef_col), sht.Cells(buttom_row, right_col)).ClearContents()
        sht.Range(sht.Cells(top_row, lef_col), sht.Cells(buttom_row, right_col)).Merge()
        self.set_cell(sheet, top_row, lef_col, data)
        return True

    @check_func(__file__, "FullExcel")
    def get_sheet_by_name(self, name):
        """
        根据名字准确查找某个sheet
        :param name:
        :return:
        """
        for i in range(1, self.book.Worksheets.Count + 1):
            if name == self.book.Worksheets(i).name:
                return i
        return 0

    @check_func(__file__, "FullExcel")
    def get_sheet_like_name(self, name):
        """
        根据名字模糊查找某个sheet
        :param name:
        :return:
        """
        for i in range(1, self.book.Worksheets.Count + 1):
            if self.book.Worksheets(i).name.find(name) > -1:
                return i
        return 0

    @check_func(__file__, "FullExcel")
    def copy_range(self, from_sheet, from_x1, from_y1, from_x2, from_y2):
        """
        拷贝sheet的某一个区域，与paste_range共用
        :param from_sheet:
        :param from_x1:
        :param from_y1:
        :param from_x2:
        :param from_y2:
        :return:
        """
        sht = self.book.Worksheets(from_sheet)
        sht.Range(sht.Cells(from_x1, from_y1), sht.Cells(from_x2, from_y2)).Select()
        self.excel.Selection.Copy()

    @check_func(__file__, "FullExcel")
    def paste_range(self, to_sheet, to_x1, to_y1, to_x2, to_y2):
        """
        黏贴sheet的某一个区域，与copy_range共用
        :param to_sheet:
        :param to_x1:
        :param to_y1:
        :param to_x2:
        :param to_y2:
        :return:
        """
        sht = self.book.Worksheets(to_sheet)
        sht.Range(sht.Cells(to_x1, to_y1), sht.Cells(to_x2, to_y2)).Select()
        self.excel.Selection.PasteSpecial(Paste=-4104)

    @check_func(__file__, "FullExcel")
    def set_border(self, sheet, top_row, lef_col, buttom_row, right_col):
        """
        设置目标sheet的某一个区域的边框
        :param sheet: 目标sheet
        :param top_row:起始行
        :param lef_col:起始列
        :param buttom_row:终止行
        :param right_col:终止列
        :return:
        """
        sht = self.book.WorkSheets(sheet)
        range = sht.Range(sht.Cells(top_row, lef_col), sht.Cells(buttom_row, right_col))
        range.Borders.LineStyle = 1
        range.Borders.Weight = 2
        range.HorizontalAlignment = -4108
        return True


# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
class FastExcel(object):
    __class_name = "FastExcel"

    @check_func(__file__, __class_name)
    def __init__(self, file_name, mode, sheet_name):
        self.file_name = file_name
        self.mode = mode
        if mode == "read":
            if not files.has_file(file_name):
                raise Exception("File not exists: %s" % file_name)
            self.excel_book = xlrd.open_workbook(file_name)
        elif mode == "write":
            if not (file_name.find("xls") > -1 and file_name.find("xlsx") == -1):
                raise Exception("FastExcel is based on xlwt, xlwt only support .xls file.")
            if not sheet_name:
                raise Exception("Full excel mode is write, need a sheet name.")
            self.excel_book = xlwt.Workbook()
            self.editing_sheet = self.excel_book.add_sheet(sheet_name)
        else:
            pass

    @check_func(__file__, __class_name)
    def close(self):
        """
        在write模式下保存文件
        :return:
        """
        if self.mode == "write":
            if self.excel_book:
                self.excel_book.save(self.file_name)

    @check_func(__file__, __class_name)
    def get_sheets_name(self):
        """
        获得所有sheet名字
        :return:
        """
        if self.mode != "read":
            raise Exception("Input mode should be read, get: %s" % self.mode)
        return self.excel_book.sheet_names()

    @check_func(__file__, __class_name)
    def get_sheets_size(self):
        """
        获得sheet表的数量
        :return:
        """
        if self.mode != "read":
            raise Exception("Input mode should be read, get: %s" % self.mode)
        return self.excel_book.nsheets

    @check_func(__file__, __class_name)
    def get_sheet_by_id(self, index):
        """
        根据index值获得某个sheet
        :param index:
        :return:
        """
        if self.mode != "read":
            raise Exception("Input mode should be read, get: %s" % self.mode)
        return self.excel_book.sheet_by_index(index - 1)

    @check_func(__file__, __class_name)
    def get_sheet_by_name(self, name):
        """
        根据名字获得某个sheet
        :param name:
        :return:
        """
        return self.excel_book.sheet_by_name(name)

    @check_func(__file__, __class_name)
    def get_row_size(self, sheet):
        """
        获得一行最高值
        :param sheet:
        :return:
        """
        if self.mode != "read":
            raise Exception("Input mode should be read, get: %s" % self.mode)
        sht = self.get_sheet_by_id(sheet)
        return sht.nrows

    @check_func(__file__, __class_name)
    def get_col_size(self, sheet):
        """
        获得一列最高值
        :param sheet:
        :return:
        """
        if self.mode != "read":
            raise Exception("Input mode should be read, get: %s" % self.mode)
        sht = self.get_sheet_by_id(sheet)
        return sht.ncols

    @check_func(__file__, __class_name)
    def get_one_row(self, sheet, index):
        """
        获得一行单元格
        :param sheet:
        :param index:
        :return:
        """
        if self.mode != "read":
            raise Exception("Input mode should be read, get: %s" % self.mode)
        sht = self.get_sheet_by_id(sheet)
        return sht.row_values(index - 1)

    @check_func(__file__, __class_name)
    def get_one_col(self, sheet, index):
        """
        获得一列单元格
        :param sheet:
        :param index:
        :return:
        """
        if self.mode != "read":
            raise Exception("Input mode should be read, get: %s" % self.mode)
        sht = self.get_sheet_by_id(sheet)
        return sht.col_values(index - 1)

    @check_func(__file__, __class_name)
    def get_one_cell(self, sheet, r_cnt, c_cnt):
        """
        获得某个单元格
        :param sheet:
        :param r_cnt:
        :param c_cnt:
        :return:
        """
        if self.mode != "read":
            raise Exception("Input mode should be read, get: %s" % self.mode)
        sht = self.get_sheet_by_id(sheet)
        return sht.cell(r_cnt - 1, c_cnt - 1)

    @check_func(__file__, __class_name)
    def get_cell(self, sheet, r_cnt, c_cnt):
        """
        获得单元格的值
        :param sheet:
        :param r_cnt:
        :param c_cnt:
        :return:
        """
        if self.mode != "read":
            raise Exception("Input mode should be read, get: %s" % self.mode)
        sht = self.get_sheet_by_id(sheet)
        return sht.cell_value(r_cnt - 1, c_cnt - 1)

    @check_func(__file__, __class_name)
    def set_cell(self, row, col, data, style=None):
        """
        设置单元格的值
        :param row:
        :param col:
        :param data:
        :param style:
        :return:
        """
        if self.mode != "write":
            raise Exception("Input mode should be write, get: %s" % self.mode)
        if style:
            self.editing_sheet.write(row - 1, col - 1, data, style)
        else:
            self.editing_sheet.write(row - 1, col - 1, data)
        return True

    @check_func(__file__, __class_name)
    def merge_cell(self, top_row, lef_col, buttom_row, right_col, data, style=None):
        """
        合并单元格，并设置值，可以通过create_style返回style进行格式调整
        :param top_row:
        :param lef_col:
        :param buttom_row:
        :param right_col:
        :param data:
        :param style:
        :return:
        """
        if self.mode != "write":
            raise Exception("Input mode should be write, get: %s" % self.mode)
        self.editing_sheet.merge(top_row - 1, buttom_row - 1, lef_col - 1, right_col - 1)
        if style:
            self.set_cell(top_row, lef_col, data, style)
        else:
            self.set_cell(top_row, lef_col, data)
        return True

    @check_func(__file__, __class_name)
    def create_style(self, desc):
        """
        create simple style use text, i.e.:
        styleBlueBkg = xlwt.easyxf('font: color-index red, bold on');
        styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour ocean_blue; font: bold on;');
        styleBold   = xlwt.easyxf('font: bold on');
        :param desc:
        :return:
        """
        if self.mode != "write":
            raise Exception("Input mode should be write, get: %s" % self.mode)
        style = xlwt.easyxf(desc)
        return style


# noinspection PyUnresolvedReferences
def main():
    import const
    # with ExcelWrapper(const.project_main_path+r"\res\datas\input.xlsx", 'read') as excel_helper:
    # print excel_helper.get_sheets_size()
    # print excel_helper.get_cell(1, 1, 1)
    # print excel_helper.get_col_size(1),"col"
    # print excel_helper.get_row_size(1,1),"row"
    # print excel_helper.get_range(1,1,1,2,3)
    # print excel_helper.set_range(1,4,4,4,5,[["a","b"]])
    # print excel_helper.set_range(1,5,1,6,3,[["a","b","e"],["c","d","f"]])
    # print excel_helper.merge_cell(1,7,1,8,2,"aa")

    with ExcelWrapper(const.project_main_path + r"\res\datas\input2.xlsx", "write", "sheet1") as excel_helper:
        print excel_helper.set_range(1, 4, 4, 4, 5, [["a", "b"]])
        print excel_helper.merge_cell(1, 7, 1, 8, 2, "aa")

        # with ExcelWrapper(const.project_main_path+r"\res\datas\input.xlsx", 'read',use_fast=True) as excel_helper:
        #     pass
        #     print excel_helper.get_sheets_size()
        #     print excel_helper.get_sheets_name()
        #     print excel_helper.get_col_size(1),"col"
        #     print excel_helper.get_row_size(1),"row"
        #     print excel_helper.get_one_col(1,1)
        #     print excel_helper.get_one_row(1,1)
        #     print excel_helper.get_one_cell(1,1,1)
        #     print excel_helper.get_cell(1,1,1)

        # with ExcelWrapper(const.project_main_path + r"\res\datas\input1.xls", 'write', sheet_name="1",
        #                   use_fast=True) as excel_helper:
        #     print excel_helper.merge_cell(9, 1, 10, 2, "aa")


if __name__ == "__main__":
    main()
