import unittest
from unittest.mock import patch


class TestAgentImports(unittest.TestCase):
    def test_imports(self):
        """Verify that necessary modules can be imported correctly."""
        try:
            from google import genai
            from mcp.server.fastmcp import FastMCP

            self.assertIsNotNone(genai)
            self.assertIsNotNone(FastMCP)
            print("🟢 Imports check passed successfully!")
        except ImportError as e:
            self.fail(f"Import failed: {e}")

    def test_server_tools_defined(self):
        """Verify that server.py compiles and exposes the expected tools."""
        # Mock FastMCP and genai.Client to avoid server run/network calls during importing
        with patch("google.genai.Client"), patch("mcp.server.fastmcp.FastMCP"):
            import server

            self.assertTrue(hasattr(server, "generate_video"))
            self.assertTrue(hasattr(server, "edit_video"))
            self.assertTrue(hasattr(server, "animate_image"))
            self.assertTrue(hasattr(server, "interpolate_images"))
            self.assertTrue(hasattr(server, "generate_with_subjects"))
            self.assertTrue(hasattr(server, "edit_user_video"))
            print("🟢 Server tools definition check passed successfully!")


if __name__ == "__main__":
    unittest.main()
