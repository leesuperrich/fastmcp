import pytest
from fastmcp.resources import FunctionResource


class TestFunctionResource:
    """Test FunctionResource functionality."""

    def test_function_resource_creation(self):
        """Test creating a FunctionResource."""

        def my_func() -> str:
            return "test content"

        resource = FunctionResource(
            uri="fn://test",
            name="test",
            description="test function",
            func=my_func,
        )
        assert str(resource.uri) == "fn://test"
        assert resource.name == "test"
        assert resource.description == "test function"
        assert resource.mime_type == "text/plain"  # default
        assert resource.func == my_func

    async def test_read_text(self):
        """Test reading text from a FunctionResource."""

        def get_data() -> str:
            return "Hello, world!"

        resource = FunctionResource(
            uri="function://test",
            name="test",
            func=get_data,
        )
        content = await resource.read()
        assert content == "Hello, world!"
        assert resource.mime_type == "text/plain"

    async def test_read_binary(self):
        """Test reading binary data from a FunctionResource."""

        def get_data() -> bytes:
            return b"Hello, world!"

        resource = FunctionResource(
            uri="function://test",
            name="test",
            func=get_data,
        )
        content = await resource.read()
        assert content == b"Hello, world!"

    async def test_json_conversion(self):
        """Test automatic JSON conversion of non-string results."""

        def get_data() -> dict:
            return {"key": "value"}

        resource = FunctionResource(
            uri="function://test",
            name="test",
            func=get_data,
        )
        content = await resource.read()
        assert '"key": "value"' in content

    async def test_error_handling(self):
        """Test error handling in FunctionResource."""

        def failing_func() -> str:
            raise ValueError("Test error")

        resource = FunctionResource(
            uri="function://test",
            name="test",
            func=failing_func,
        )
        with pytest.raises(ValueError, match="Error reading resource function://test"):
            await resource.read()

    async def test_custom_type_conversion(self):
        """Test handling of custom types."""

        class CustomData:
            def __str__(self) -> str:
                return "custom data"

        def get_data() -> CustomData:
            return CustomData()

        resource = FunctionResource(
            uri="function://test",
            name="test",
            func=get_data,
        )
        content = await resource.read()
        assert isinstance(content, str)
