# pyvider-hcl

Comprehensive HCL (HashiCorp Configuration Language) parsing and generation with seamless CTY type system integration for the Provide Foundry.

## Overview

`pyvider-hcl` provides complete HCL 2.x parsing and generation capabilities with deep integration into the pyvider CTY type system. It enables parsing HCL configurations into type-safe CTY values and generating HCL from CTY structures.

### Key Features

- **📄 HCL 2.x Compatibility**: Full support for HCL 2.x specification
- **🔗 CTY Integration**: Seamless conversion between HCL values and CTY types
- **🧮 Expression Evaluation**: Support for HCL expressions, functions, and variables
- **📝 Template Processing**: HCL template support with variable substitution
- **🎯 Error Handling**: Rich error messages with source location context
- **🌍 Unicode Support**: Full Unicode support in configuration files

## Installation

```bash
# Basic installation
pip install pyvider-hcl

# With all extras for full functionality
pip install pyvider-hcl[all]
```

## Quick Start

### Parsing HCL Files

```python
from pyvider.hcl import parse_hcl_file, parse_hcl_string

# Parse HCL file
config = parse_hcl_file("terraform.tf")

# Parse HCL string
hcl_content = '''
variable "instance_count" {
  description = "Number of instances to create"
  type        = number
  default     = 3
}

resource "aws_instance" "web" {
  count         = var.instance_count
  ami           = "ami-12345678"
  instance_type = "t2.micro"

  tags = {
    Name        = "web-${count.index}"
    Environment = "production"
  }
}
'''

config = parse_hcl_string(hcl_content)
print(config.variables["instance_count"].default.value)  # 3
print(config.resources["aws_instance"]["web"].count)     # var.instance_count
```

### Generating HCL

```python
from pyvider.hcl import HCLGenerator
from pyvider.cty import CtyString, CtyNumber, CtyMap

# Create HCL generator
generator = HCLGenerator()

# Add variable
generator.add_variable("region", {
    "description": CtyString("AWS region"),
    "type": CtyString("string"),
    "default": CtyString("us-west-2")
})

# Add resource
generator.add_resource("aws_instance", "web", {
    "ami": CtyString("ami-12345678"),
    "instance_type": CtyString("t2.micro"),
    "tags": CtyMap({
        "Name": CtyString("web-server"),
        "Environment": CtyString("production")
    })
})

# Generate HCL
hcl_output = generator.to_hcl()
print(hcl_output)
```

## Parser Components

### HCL Parser

Core HCL parsing functionality:

```python
from pyvider.hcl.parser import HCLParser

# Create parser with options
parser = HCLParser(
    allow_missing_variables=True,
    strict_mode=False,
    unicode_support=True
)

# Parse configuration
try:
    config = parser.parse_file("config.hcl")

    # Access parsed elements
    variables = config.variables
    resources = config.resources
    data_sources = config.data_sources
    locals = config.locals
    outputs = config.outputs

except HCLParseError as e:
    print(f"Parse error at line {e.line}: {e.message}")
    print(f"Context: {e.context}")
```

### Expression Evaluation

HCL expression evaluation with variable resolution:

```python
from pyvider.hcl.expressions import ExpressionEvaluator
from pyvider.cty import CtyString, CtyNumber, CtyMap

# Create evaluator with context
evaluator = ExpressionEvaluator()

# Set variable context
evaluator.set_variables({
    "region": CtyString("us-west-2"),
    "instance_count": CtyNumber(3),
    "tags": CtyMap({
        "Environment": CtyString("production"),
        "Team": CtyString("platform")
    })
})

# Evaluate expressions
region_expr = 'var.region'
result = evaluator.evaluate(region_expr)
print(result.value)  # "us-west-2"

# Complex expressions
complex_expr = '${var.tags.Environment}-${var.region}'
result = evaluator.evaluate(complex_expr)
print(result.value)  # "production-us-west-2"

# Function calls
length_expr = 'length(var.tags)'
result = evaluator.evaluate(length_expr)
print(result.value)  # 2
```

### Variable Resolution

Resolve variable references within configurations:

```python
from pyvider.hcl.variables import VariableResolver

# Create resolver
resolver = VariableResolver()

# Add variable definitions
resolver.add_variable("environment", CtyString("production"))
resolver.add_variable("region", CtyString("us-west-2"))

# Add local values
resolver.add_local("common_tags", CtyMap({
    "Environment": CtyString("${var.environment}"),
    "Region": CtyString("${var.region}")
}))

# Resolve references
resolved_tags = resolver.resolve("local.common_tags")
print(resolved_tags["Environment"].value)  # "production"
print(resolved_tags["Region"].value)      # "us-west-2"
```

## Configuration Elements

### Variables

Parse and work with HCL variables:

```python
from pyvider.hcl import parse_hcl_string

hcl_content = '''
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"

  validation {
    condition     = contains(["t2.micro", "t2.small", "t2.medium"], var.instance_type)
    error_message = "Instance type must be t2.micro, t2.small, or t2.medium."
  }
}

variable "instance_count" {
  description = "Number of instances"
  type        = number
  default     = 1

  validation {
    condition     = var.instance_count >= 1 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}
'''

config = parse_hcl_string(hcl_content)

# Access variable properties
instance_type_var = config.variables["instance_type"]
print(instance_type_var.description.value)  # "EC2 instance type"
print(instance_type_var.type.value)         # "string"
print(instance_type_var.default.value)      # "t2.micro"
print(len(instance_type_var.validations))   # 1

# Access validation rules
validation = instance_type_var.validations[0]
print(validation.condition)                 # Expression object
print(validation.error_message.value)       # "Instance type must be..."
```

### Resources

Parse resource blocks with complex configurations:

```python
hcl_content = '''
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name

  vpc_security_group_ids = [aws_security_group.web.id]
  subnet_id              = data.aws_subnet.public.id

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    environment = var.environment
    app_name    = var.app_name
  }))

  root_block_device {
    volume_type = "gp3"
    volume_size = 20
    encrypted   = true
  }

  ebs_block_device {
    device_name = "/dev/sdf"
    volume_type = "gp3"
    volume_size = 100
    encrypted   = true
  }

  tags = merge(local.common_tags, {
    Name = "${var.environment}-web-server"
    Type = "web"
  })

  lifecycle {
    create_before_destroy = true
    ignore_changes = [
      ami,
      user_data,
    ]
  }
}
'''

config = parse_hcl_string(hcl_content)

# Access resource configuration
web_resource = config.resources["aws_instance"]["web"]
print(web_resource.ami)                    # var.ami_id (Expression)
print(web_resource.instance_type)          # var.instance_type (Expression)

# Access nested blocks
root_block = web_resource.root_block_device[0]
print(root_block.volume_type.value)        # "gp3"
print(root_block.volume_size.value)        # 20
print(root_block.encrypted.value)          # True

# Access lifecycle configuration
lifecycle = web_resource.lifecycle
print(lifecycle.create_before_destroy.value)  # True
print([change.value for change in lifecycle.ignore_changes])  # ["ami", "user_data"]
```

### Data Sources

Parse data source blocks:

```python
hcl_content = '''
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

data "aws_availability_zones" "available" {
  state = "available"

  filter {
    name   = "opt-in-status"
    values = ["opt-in-not-required"]
  }
}
'''

config = parse_hcl_string(hcl_content)

# Access data sources
ubuntu_ami = config.data_sources["aws_ami"]["ubuntu"]
print(ubuntu_ami.most_recent.value)        # True
print(ubuntu_ami.owners[0].value)          # "099720109477"

# Access filter blocks
filters = ubuntu_ami.filters
name_filter = filters[0]
print(name_filter.name.value)              # "name"
print(name_filter.values[0].value)         # "ubuntu/images/hvm-ssd/..."
```

### Locals and Outputs

Parse local values and output blocks:

```python
hcl_content = '''
locals {
  environment = "production"
  region      = "us-west-2"

  common_tags = {
    Environment = local.environment
    Region      = local.region
    ManagedBy   = "terraform"
  }

  instance_count = var.high_availability ? 3 : 1
}

output "instance_ips" {
  description = "Public IP addresses of instances"
  value       = aws_instance.web[*].public_ip
  sensitive   = false
}

output "database_password" {
  description = "Database password"
  value       = random_password.db_password.result
  sensitive   = true
}
'''

config = parse_hcl_string(hcl_content)

# Access locals
locals_block = config.locals
print(locals_block["environment"].value)   # "production"
print(locals_block["region"].value)        # "us-west-2"

# Access outputs
instance_ips_output = config.outputs["instance_ips"]
print(instance_ips_output.description.value)  # "Public IP addresses of instances"
print(instance_ips_output.sensitive.value)    # False

db_password_output = config.outputs["database_password"]
print(db_password_output.sensitive.value)     # True
```

## Template Processing

### Template Engine

Process HCL templates with variable substitution:

```python
from pyvider.hcl.templates import HCLTemplateEngine
from pyvider.cty import CtyString, CtyMap, CtyList

# Create template engine
engine = HCLTemplateEngine()

# Define template
template_content = '''
resource "${resource_type}" "${resource_name}" {
  %{ for key, value in attributes ~}
  ${key} = ${jsonencode(value)}
  %{ endfor ~}

  tags = merge(local.common_tags, {
    %{ for tag_key, tag_value in additional_tags ~}
    ${tag_key} = ${jsonencode(tag_value)}
    %{ endfor ~}
  })
}
'''

# Set template variables
engine.set_variables({
    "resource_type": CtyString("aws_instance"),
    "resource_name": CtyString("web"),
    "attributes": CtyMap({
        "ami": CtyString("ami-12345678"),
        "instance_type": CtyString("t2.micro")
    }),
    "additional_tags": CtyMap({
        "Environment": CtyString("production"),
        "Application": CtyString("web-server")
    })
})

# Process template
result = engine.process(template_content)
print(result)
```

### Template Functions

Use HCL template functions:

```python
from pyvider.hcl.templates import TemplateFunctions

# Create function context
functions = TemplateFunctions()

# Built-in functions
result = functions.call("upper", [CtyString("hello")])
print(result.value)  # "HELLO"

result = functions.call("join", [CtyString(","), CtyList([
    CtyString("a"), CtyString("b"), CtyString("c")
])])
print(result.value)  # "a,b,c"

result = functions.call("length", [CtyList([
    CtyString("x"), CtyString("y"), CtyString("z")
])])
print(result.value)  # 3

# Custom functions
def custom_prefix(prefix, value):
    """Add prefix to string value."""
    return CtyString(f"{prefix.value}-{value.value}")

functions.register("prefix", custom_prefix)

result = functions.call("prefix", [
    CtyString("prod"),
    CtyString("web-server")
])
print(result.value)  # "prod-web-server"
```

## Error Handling

### Parse Errors

Comprehensive error reporting with source location:

```python
from pyvider.hcl import parse_hcl_string, HCLParseError

invalid_hcl = '''
variable "name" {
  description = "Resource name"
  type        = string
  default     = missing_quotes
}
'''

try:
    config = parse_hcl_string(invalid_hcl)
except HCLParseError as e:
    print(f"Parse error: {e.message}")
    print(f"Location: line {e.line}, column {e.column}")
    print(f"Context: {e.context}")
    print(f"Suggestion: {e.suggestion}")

    # Error details
    print(f"Error type: {e.error_type}")
    print(f"Source snippet:")
    for i, line in enumerate(e.source_lines, 1):
        marker = ">>> " if i == e.line else "    "
        print(f"{marker}{i:3}: {line}")
```

### Validation Errors

Variable and expression validation:

```python
from pyvider.hcl import HCLValidator, ValidationError

# Create validator
validator = HCLValidator()

# Validate configuration
try:
    validator.validate_file("terraform.tf")
    print("Configuration is valid")
except ValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Path: {e.path}")
    print(f"Rule: {e.rule}")

    # Multiple errors
    for error in e.errors:
        print(f"  - {error.message} at {error.path}")
```

## Advanced Features

### Custom Functions

Extend HCL with custom functions:

```python
from pyvider.hcl.functions import FunctionRegistry
from pyvider.cty import CtyString, CtyNumber, CtyBool

# Create function registry
registry = FunctionRegistry()

# Register custom function
@registry.function("validate_email")
def validate_email(email: CtyString) -> CtyBool:
    """Validate email address format."""
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = re.match(email_pattern, email.value) is not None
    return CtyBool(is_valid)

@registry.function("calculate_cost")
def calculate_cost(hours: CtyNumber, rate: CtyNumber) -> CtyNumber:
    """Calculate cost based on hours and rate."""
    total_cost = hours.value * rate.value
    return CtyNumber(round(total_cost, 2))

# Use in HCL expressions
hcl_content = '''
variable "admin_email" {
  description = "Administrator email"
  type        = string

  validation {
    condition     = validate_email(var.admin_email)
    error_message = "Admin email must be valid email address."
  }
}

locals {
  monthly_cost = calculate_cost(720, 0.10)  # 720 hours * $0.10/hour
}
'''

# Parse with custom functions
parser = HCLParser(function_registry=registry)
config = parser.parse_string(hcl_content)
```

### Configuration Loading

Load and merge multiple configuration files:

```python
from pyvider.hcl.loader import ConfigurationLoader

# Create loader
loader = ConfigurationLoader()

# Load configuration from multiple sources
config = loader.load_directory("terraform/")

# Load with variable overrides
config = loader.load_files([
    "main.tf",
    "variables.tf",
    "outputs.tf"
], variable_overrides={
    "environment": CtyString("staging"),
    "region": CtyString("us-east-1")
})

# Load with validation
config = loader.load_and_validate(
    "terraform.tf",
    schema_file="schema.json"
)
```

### Schema Integration

Define and validate HCL schemas:

```python
from pyvider.hcl.schema import HCLSchema, SchemaValidator

# Define schema
schema = HCLSchema({
    "variables": {
        "environment": {
            "type": "string",
            "required": True,
            "allowed_values": ["dev", "staging", "production"]
        },
        "instance_count": {
            "type": "number",
            "required": False,
            "default": 1,
            "minimum": 1,
            "maximum": 10
        }
    },
    "resources": {
        "aws_instance": {
            "required_attributes": ["ami", "instance_type"],
            "optional_attributes": ["tags", "user_data"],
            "blocks": {
                "root_block_device": {
                    "max_items": 1
                }
            }
        }
    }
})

# Validate configuration against schema
validator = SchemaValidator(schema)
try:
    validator.validate(config)
    print("Configuration matches schema")
except ValidationError as e:
    print(f"Schema validation failed: {e}")
```

## Performance Optimization

### Lazy Parsing

Parse large configurations efficiently:

```python
from pyvider.hcl import LazyHCLParser

# Create lazy parser
parser = LazyHCLParser()

# Parse large configuration
config = parser.parse_file("large_terraform_config.tf")

# Access elements on-demand (parsed when accessed)
variables = config.variables  # Parsed now
resources = config.resources  # Parsed now

# Specific resource (parsed individually)
web_instance = config.resources["aws_instance"]["web"]
```

### Caching

Cache parsed configurations:

```python
from pyvider.hcl import CachedHCLParser

# Create parser with caching
parser = CachedHCLParser(
    cache_dir="/tmp/hcl_cache",
    cache_ttl=3600  # 1 hour
)

# First parse (cached)
config1 = parser.parse_file("terraform.tf")

# Second parse (from cache)
config2 = parser.parse_file("terraform.tf")

assert config1 is config2  # Same cached instance
```

## Integration Examples

### With pyvider

Use HCL parsing in Terraform providers:

```python
from pyvider import resource
from pyvider.hcl import parse_hcl_string

@resource
class TerraformConfig:
    """Resource for managing Terraform configurations."""

    content: CtyString = Attribute(
        description="HCL configuration content",
        required=True
    )

    def validate_config(self, config):
        """Validate HCL configuration."""
        try:
            parsed = parse_hcl_string(config.content.value)
            return {"valid": True, "parsed": parsed}
        except HCLParseError as e:
            return {
                "valid": False,
                "error": str(e),
                "line": e.line,
                "column": e.column
            }

    def create(self, config) -> dict:
        """Create configuration resource."""
        validation = self.validate_config(config)
        if not validation["valid"]:
            raise ResourceError(f"Invalid HCL: {validation['error']}")

        # Store configuration
        config_id = self.provider.client.store_config(
            content=config.content.value
        )

        return {
            "id": config_id,
            "content": config.content.value,
            "valid": True
        }
```

### With Configuration Management

Parse Terraform configurations for analysis:

```python
from pyvider.hcl import parse_hcl_file

def analyze_terraform_config(config_file):
    """Analyze Terraform configuration."""
    config = parse_hcl_file(config_file)

    analysis = {
        "variables": len(config.variables),
        "resources": {},
        "data_sources": {},
        "outputs": len(config.outputs)
    }

    # Analyze resources by type
    for resource_type, resources in config.resources.items():
        analysis["resources"][resource_type] = len(resources)

    # Analyze data sources by type
    for data_type, data_sources in config.data_sources.items():
        analysis["data_sources"][data_type] = len(data_sources)

    return analysis

# Analyze configuration
analysis = analyze_terraform_config("main.tf")
print(f"Found {analysis['variables']} variables")
print(f"Resource types: {list(analysis['resources'].keys())}")
```

## Best Practices

1. **Use type-safe parsing** - Always parse into CTY types for validation
2. **Handle errors gracefully** - Provide clear error messages with context
3. **Validate configurations** - Use schema validation for robust parsing
4. **Cache when possible** - Cache parsed configurations for performance
5. **Unicode support** - Ensure proper Unicode handling in configurations
6. **Test thoroughly** - Test with various HCL syntax patterns
7. **Performance aware** - Use lazy parsing for large configurations

## Related Packages

- **[pyvider-cty](pyvider-cty.md)**: CTY type system for values
- **[pyvider](pyvider.md)**: Core framework using HCL parsing
- **[provide-foundation](foundation.md)**: Foundation services

---

pyvider-hcl provides comprehensive HCL parsing and generation capabilities for the Provide Foundry, enabling seamless integration between Terraform configurations and Python provider development.