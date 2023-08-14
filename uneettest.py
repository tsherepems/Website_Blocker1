import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import tkinter as tk
import subprocess
from Website_Blocker import WebsiteBlockerApp

class TestWebsiteBlockerApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.app = WebsiteBlockerApp(cls.root)
        
    def test_check_password(self):
        # Test correct password
        with patch('tkinter.simpledialog.askstring', return_value='your_password'):
            with patch('tkinter.messagebox.showinfo') as mock_showinfo:
                self.app.check_password()
                mock_showinfo.assert_called_with('Password Set', 'Password set successfully.')

    @patch('tkinter.simpledialog.askstring', return_value='invalid_password')
    @patch('tkinter.messagebox.showerror')
    def test_check_password_incorrect(self, mock_showerror, mock_askstring):
        with self.assertRaises(SystemExit):
            self.app.check_password()
        mock_showerror.assert_called_with('Incorrect Password', 'Invalid password.')

    @patch('tkinter.messagebox.askokcancel', return_value=True)
    @patch('tkinter.messagebox.showinfo')
    def test_schedule_blocking(self, mock_showinfo, mock_askokcancel):
        # Mock schedule_time_entry to have a future datetime
        future_time = datetime.now() + timedelta(hours=1)
        self.app.schedule_time_entry = MagicMock(get=lambda: future_time.strftime('%Y-%m-%d %H:%M:%S'))

        # Mock the after method of root
        self.app.root.after = MagicMock()

        self.app.schedule_blocking()
        self.assertTrue(self.app.root.after.called)
        mock_showinfo.assert_called_with('Schedule Set', 'The blocking is scheduled successfully.')

    @patch('tkinter.messagebox.askokcancel', return_value=True)
    @patch('tkinter.messagebox.showinfo')
    def test_schedule_unblocking(self, mock_showinfo, mock_askokcancel):
        # Mock schedule_time_entry to have a future datetime
        future_time = datetime.now() + timedelta(hours=1)
        self.app.schedule_time_entry = MagicMock(get=lambda: future_time.strftime('%Y-%m-%d %H:%M:%S'))

        # Mock the after method of root
        self.app.root.after = MagicMock()

        self.app.schedule_unblocking()
        self.assertTrue(self.app.root.after.called)
        mock_showinfo.assert_called_with('Schedule Set', 'The unblocking is scheduled successfully.')

    @patch('subprocess.run', return_value=MagicMock(returncode=0, stdout='Ping success'))
    def test_confirm_blocking_status(self, mock_run):
        # Mock entry with a site to check
        self.app.entry = MagicMock(get=lambda: 'example.com')

        # Mock output_text
        self.app.output_text = MagicMock()

        self.app.confirm_blocking_status()

        # Asserts for text widget
        self.assertTrue(self.app.output_text.delete.called)
        self.assertTrue(self.app.output_text.insert.called)

    @patch('subprocess.run', side_effect=subprocess.CalledProcessError(returncode=1, cmd='ping'))
    def test_confirm_blocking_status_failure(self, mock_run):
        # Mock entry with a site to check
        self.app.entry = MagicMock(get=lambda: 'example.com')

        # Mock output_text
        self.app.output_text = MagicMock()

        self.app.confirm_blocking_status()

        # Asserts for text widget
        self.assertTrue(self.app.output_text.delete.called)
        self.assertTrue(self.app.output_text.insert.called)

if __name__ == '__main__':
    unittest.main()
