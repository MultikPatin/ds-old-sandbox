DATETIME_PYDANTIC_FIELD_DESCRIPTION = """
The following formats are accepted:
<ul>
  <li><code>YYYY-MM-DD[T]HH:MM[:SS[.ffffff]][Z or [±]HH[:]MM]</code></li>
  <li><code>int</code> or <code>float</code> as a string (assumed as Unix time)</li>
</ul>
"""  # noqa: E501
DATETIME_PYDANTIC_FIELD_EXAMPLES = ["2024-04-19T17:17:31.711", "1746115032"]

DATE_PYDANTIC_FIELD_DESCRIPTION = """
The following formats are accepted:
<ul>
  <li><code>YYYY-MM-DD</code></li>
  <li><code>int</code> or <code>float</code> as a string (assumed as Unix time)</li>
</ul>
"""  # noqa: E501
DATE_PYDANTIC_FIELD_EXAMPLES = ["2024-04-19", "1713474000"]

TIME_PYDANTIC_FIELD_DESCRIPTION = """
The following formats are accepted:
<ul>
  <li><code>HH:MM[:SS[.ffffff]][Z or [±]HH[:]MM]</code></li>
</ul>
"""
TIME_PYDANTIC_FIELD_EXAMPLES = ["17:31.711"]
