#include <windows.h>
#include <commctrl.h>
#include <stdio.h>
#include "Student.h"
#include "resource.h"

using namespace std;

HINSTANCE hInst;

/** \brief ���ڻص�����
 *      һ�����¼���Ӧ��ϵͳ����ô˺�����
 *
 * \param hwndDlg ���ھ�� 32λ�޷�������
 * \param uMsg ��Ϣ����
 * \param wParam �¼���Ϣ
 * \param lParam �¼���Ϣ
 * \return
 *
 */
BOOL CALLBACK DlgMain(HWND hwndDlg, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    switch(uMsg)
    {
    case WM_INITDIALOG: /**< ���ڳ�ʼ���¼� */
    {
    }
    return TRUE;

    case WM_CLOSE:  /**< ���ڹر��¼� */
    {
        EndDialog(hwndDlg, 0);
    }
    return TRUE;

    case WM_COMMAND:    /**< �����¼� */
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
