#include <windows.h>
#include <commctrl.h>
#include <stdio.h>
#include "Student.h"
#include "resource.h"

using namespace std;

HINSTANCE hInst;

/** \brief 窗口回调函数
 *      一旦有事件响应，系统会调用此函数。
 *
 * \param hwndDlg 窗口句柄 32位无符号整数
 * \param uMsg 消息类型
 * \param wParam 事件信息
 * \param lParam 事件信息
 * \return
 *
 */
BOOL CALLBACK DlgMain(HWND hwndDlg, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    switch(uMsg)
    {
    case WM_INITDIALOG: /**< 窗口初始化事件 */
    {
    }
    return TRUE;

    case WM_CLOSE:  /**< 窗口关闭事件 */
    {
        EndDialog(hwndDlg, 0);
    }
    return TRUE;

    case WM_COMMAND:    /**< 单击事件 */
    {
        switch(LOWORD(wParam))
        {

        }
    }
    return TRUE;
    }
    return FALSE;
}


int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd)
{
    hInst=hInstance;

    InitCommonControls();
    return DialogBox(hInst, MAKEINTRESOURCE(DLG_MAIN), NULL, (DLGPROC)DlgMain);
}
