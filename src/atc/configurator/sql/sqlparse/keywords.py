#
# Copyright (C) 2009-2020 the sqlparse authors and contributors
# <see AUTHORS file>
#
# This module is part of python-sqlparse and is released under
# the BSD License: https://opensource.org/licenses/BSD-3-Clause

from atc.configurator.sql.sqlparse import tokens

# object() only supports "is" and is useful as a marker
# use this marker to specify that the given regex in SQL_REGEX
# shall be processed further through a lookup in the KEYWORDS dictionaries
PROCESS_AS_KEYWORD = object()


SQL_REGEX = [
    (r"(--|# )\+.*?(\r\n|\r|\n|$)", tokens.Comment.Single.Hint),
    (r"/\*\+[\s\S]*?\*/", tokens.Comment.Multiline.Hint),
    (r"(--|# ).*?(\r\n|\r|\n|$)", tokens.Comment.Single),
    (r"/\*[\s\S]*?\*/", tokens.Comment.Multiline),
    (r"(\r\n|\r|\n)", tokens.Newline),
    (r"\s+", tokens.Whitespace),
    (r":=", tokens.Assignment),
    (r"::", tokens.Punctuation),
    (r"\*", tokens.Wildcard),
    (r"`(``|[^`])*`", tokens.Name),
    (r"´(´´|[^´])*´", tokens.Name),
    (r"((?<!\S)\$(?:[_A-ZÀ-Ü]\w*)?\$)[\s\S]*?\1", tokens.Literal),
    (r"\?", tokens.Name.Placeholder),
    (r"%(\(\w+\))?s", tokens.Name.Placeholder),
    (r"(?<!\w)[$:?]\w+", tokens.Name.Placeholder),
    (r"\\\w+", tokens.Command),
    (r"(NOT\s+)?(IN)\b", tokens.Operator.Comparison),
    # FIXME(andi): VALUES shouldn't be listed here
    # see https://github.com/andialbrecht/sqlparse/pull/64
    # AS and IN are special, it may be followed by a parenthesis, but
    # are never functions, see issue183 and issue507
    (r"(CASE|IN|VALUES|USING|FROM|AS)\b", tokens.Keyword),
    (r"(@|##|#)[A-ZÀ-Ü]\w+", tokens.Name),
    # see issue #39
    # Spaces around period `schema . name` are valid identifier
    # TODO: Spaces before period not implemented
    (r"[A-ZÀ-Ü]\w*(?=\s*\.)", tokens.Name),  # 'Name'.
    # FIXME(atronah): never match,
    # because `re.match` doesn't work with look-behind regexp feature
    (r"(?<=\.)[A-ZÀ-Ü]\w*", tokens.Name),  # .'Name'
    (r"[A-ZÀ-Ü]\w*(?=\()", tokens.Name),  # side effect: change kw to func
    (r"-?0x[\dA-F]+", tokens.Number.Hexadecimal),
    (r"-?\d+(\.\d+)?E-?\d+", tokens.Number.Float),
    (r"(?![_A-ZÀ-Ü])-?(\d+(\.\d*)|\.\d+)(?![_A-ZÀ-Ü])", tokens.Number.Float),
    (r"(?![_A-ZÀ-Ü])-?\d+(?![_A-ZÀ-Ü])", tokens.Number.Integer),
    (r"'(''|\\\\|\\'|[^'])*'", tokens.String.Single),
    # not a real string literal in ANSI SQL:
    (r'"(""|\\\\|\\"|[^"])*"', tokens.String.Symbol),
    (r'(""|".*?[^\\]")', tokens.String.Symbol),
    # sqlite names can be escaped with [square brackets]. left bracket
    # cannot be preceded by word character or a right bracket --
    # otherwise it's probably an array index
    (r"(?<![\w\])])(\[[^\]\[]+\])", tokens.Name),
    (
        r"((LEFT\s+|RIGHT\s+|FULL\s+)?(INNER\s+|OUTER\s+|STRAIGHT\s+)?"
        r"|(CROSS\s+|NATURAL\s+)?)?JOIN\b",
        tokens.Keyword,
    ),
    (r"END(\s+IF|\s+LOOP|\s+WHILE)?\b", tokens.Keyword),
    (r"NOT\s+NULL\b", tokens.Keyword),
    (r"NULLS\s+(FIRST|LAST)\b", tokens.Keyword),
    (r"UNION\s+ALL\b", tokens.Keyword),
    (r"CREATE(\s+OR\s+REPLACE)?\b", tokens.Keyword.DDL),
    (r"DOUBLE\s+PRECISION\b", tokens.Name.Builtin),
    (r"GROUP\s+BY\b", tokens.Keyword),
    (r"ORDER\s+BY\b", tokens.Keyword),
    (r"HANDLER\s+FOR\b", tokens.Keyword),
    (
        r"(LATERAL\s+VIEW\s+)" r"(EXPLODE|INLINE|PARSE_URL_TUPLE|POSEXPLODE|STACK)\b",
        tokens.Keyword,
    ),
    (r"(AT|WITH')\s+TIME\s+ZONE\s+'[^']+'", tokens.Keyword.TZCast),
    (r"(NOT\s+)?(LIKE|ILIKE|RLIKE)\b", tokens.Operator.Comparison),
    (r"(NOT\s+)?(REGEXP)\b", tokens.Operator.Comparison),
    # Check for keywords, also returns tokens.Name if regex matches
    # but the match isn't a keyword.
    (r"[0-9_\w][_$#\w]*", PROCESS_AS_KEYWORD),
    (r"[;:()\[\],\.]", tokens.Punctuation),
    (r"[<>=~!]+", tokens.Operator.Comparison),
    (r"[+/@#%^&|^-]+", tokens.Operator),
]

KEYWORDS = {
    "ABORT": tokens.Keyword,
    "ABS": tokens.Keyword,
    "ABSOLUTE": tokens.Keyword,
    "ACCESS": tokens.Keyword,
    "ADA": tokens.Keyword,
    "ADD": tokens.Keyword,
    "ADMIN": tokens.Keyword,
    "AFTER": tokens.Keyword,
    "AGGREGATE": tokens.Keyword,
    "ALIAS": tokens.Keyword,
    "ALL": tokens.Keyword,
    "ALLOCATE": tokens.Keyword,
    "ANALYSE": tokens.Keyword,
    "ANALYZE": tokens.Keyword,
    "ANY": tokens.Keyword,
    "ARRAYLEN": tokens.Keyword,
    "ARE": tokens.Keyword,
    "ASC": tokens.Keyword.Order,
    "ASENSITIVE": tokens.Keyword,
    "ASSERTION": tokens.Keyword,
    "ASSIGNMENT": tokens.Keyword,
    "ASYMMETRIC": tokens.Keyword,
    "AT": tokens.Keyword,
    "ATOMIC": tokens.Keyword,
    "AUDIT": tokens.Keyword,
    "AUTHORIZATION": tokens.Keyword,
    "AUTO_INCREMENT": tokens.Keyword,
    "AVG": tokens.Keyword,
    "BACKWARD": tokens.Keyword,
    "BEFORE": tokens.Keyword,
    "BEGIN": tokens.Keyword,
    "BETWEEN": tokens.Keyword,
    "BITVAR": tokens.Keyword,
    "BIT_LENGTH": tokens.Keyword,
    "BOTH": tokens.Keyword,
    "BREADTH": tokens.Keyword,
    # 'C': tokens.Keyword,  # most likely this is an alias
    "CACHE": tokens.Keyword,
    "CALL": tokens.Keyword,
    "CALLED": tokens.Keyword,
    "CARDINALITY": tokens.Keyword,
    "CASCADE": tokens.Keyword,
    "CASCADED": tokens.Keyword,
    "CAST": tokens.Keyword,
    "CATALOG": tokens.Keyword,
    "CATALOG_NAME": tokens.Keyword,
    "CHAIN": tokens.Keyword,
    "CHARACTERISTICS": tokens.Keyword,
    "CHARACTER_LENGTH": tokens.Keyword,
    "CHARACTER_SET_CATALOG": tokens.Keyword,
    "CHARACTER_SET_NAME": tokens.Keyword,
    "CHARACTER_SET_SCHEMA": tokens.Keyword,
    "CHAR_LENGTH": tokens.Keyword,
    "CHARSET": tokens.Keyword,
    "CHECK": tokens.Keyword,
    "CHECKED": tokens.Keyword,
    "CHECKPOINT": tokens.Keyword,
    "CLASS": tokens.Keyword,
    "CLASS_ORIGIN": tokens.Keyword,
    "CLOB": tokens.Keyword,
    "CLOSE": tokens.Keyword,
    "CLUSTER": tokens.Keyword,
    "COALESCE": tokens.Keyword,
    "COBOL": tokens.Keyword,
    "COLLATE": tokens.Keyword,
    "COLLATION": tokens.Keyword,
    "COLLATION_CATALOG": tokens.Keyword,
    "COLLATION_NAME": tokens.Keyword,
    "COLLATION_SCHEMA": tokens.Keyword,
    "COLLECT": tokens.Keyword,
    "COLUMN": tokens.Keyword,
    "COLUMN_NAME": tokens.Keyword,
    "COMPRESS": tokens.Keyword,
    "COMMAND_FUNCTION": tokens.Keyword,
    "COMMAND_FUNCTION_CODE": tokens.Keyword,
    "COMMENT": tokens.Keyword,
    "COMMIT": tokens.Keyword.DML,
    "COMMITTED": tokens.Keyword,
    "COMPLETION": tokens.Keyword,
    "CONCURRENTLY": tokens.Keyword,
    "CONDITION_NUMBER": tokens.Keyword,
    "CONNECT": tokens.Keyword,
    "CONNECTION": tokens.Keyword,
    "CONNECTION_NAME": tokens.Keyword,
    "CONSTRAINT": tokens.Keyword,
    "CONSTRAINTS": tokens.Keyword,
    "CONSTRAINT_CATALOG": tokens.Keyword,
    "CONSTRAINT_NAME": tokens.Keyword,
    "CONSTRAINT_SCHEMA": tokens.Keyword,
    "CONSTRUCTOR": tokens.Keyword,
    "CONTAINS": tokens.Keyword,
    "CONTINUE": tokens.Keyword,
    "CONVERSION": tokens.Keyword,
    "CONVERT": tokens.Keyword,
    "COPY": tokens.Keyword,
    "CORRESPONDING": tokens.Keyword,
    "COUNT": tokens.Keyword,
    "CREATEDB": tokens.Keyword,
    "CREATEUSER": tokens.Keyword,
    "CROSS": tokens.Keyword,
    "CUBE": tokens.Keyword,
    "CURRENT": tokens.Keyword,
    "CURRENT_DATE": tokens.Keyword,
    "CURRENT_PATH": tokens.Keyword,
    "CURRENT_ROLE": tokens.Keyword,
    "CURRENT_TIME": tokens.Keyword,
    "CURRENT_TIMESTAMP": tokens.Keyword,
    "CURRENT_USER": tokens.Keyword,
    "CURSOR": tokens.Keyword,
    "CURSOR_NAME": tokens.Keyword,
    "CYCLE": tokens.Keyword,
    "DATA": tokens.Keyword,
    "DATABASE": tokens.Keyword,
    "DATETIME_INTERVAL_CODE": tokens.Keyword,
    "DATETIME_INTERVAL_PRECISION": tokens.Keyword,
    "DAY": tokens.Keyword,
    "DEALLOCATE": tokens.Keyword,
    "DECLARE": tokens.Keyword,
    "DEFAULT": tokens.Keyword,
    "DEFAULTS": tokens.Keyword,
    "DEFERRABLE": tokens.Keyword,
    "DEFERRED": tokens.Keyword,
    "DEFINED": tokens.Keyword,
    "DEFINER": tokens.Keyword,
    "DELIMITER": tokens.Keyword,
    "DELIMITERS": tokens.Keyword,
    "DEREF": tokens.Keyword,
    "DESC": tokens.Keyword.Order,
    "DESCRIBE": tokens.Keyword,
    "DESCRIPTOR": tokens.Keyword,
    "DESTROY": tokens.Keyword,
    "DESTRUCTOR": tokens.Keyword,
    "DETERMINISTIC": tokens.Keyword,
    "DIAGNOSTICS": tokens.Keyword,
    "DICTIONARY": tokens.Keyword,
    "DISABLE": tokens.Keyword,
    "DISCONNECT": tokens.Keyword,
    "DISPATCH": tokens.Keyword,
    "DIV": tokens.Operator,
    "DO": tokens.Keyword,
    "DOMAIN": tokens.Keyword,
    "DYNAMIC": tokens.Keyword,
    "DYNAMIC_FUNCTION": tokens.Keyword,
    "DYNAMIC_FUNCTION_CODE": tokens.Keyword,
    "EACH": tokens.Keyword,
    "ENABLE": tokens.Keyword,
    "ENCODING": tokens.Keyword,
    "ENCRYPTED": tokens.Keyword,
    "END-EXEC": tokens.Keyword,
    "ENGINE": tokens.Keyword,
    "EQUALS": tokens.Keyword,
    "ESCAPE": tokens.Keyword,
    "EVERY": tokens.Keyword,
    "EXCEPT": tokens.Keyword,
    "EXCEPTION": tokens.Keyword,
    "EXCLUDING": tokens.Keyword,
    "EXCLUSIVE": tokens.Keyword,
    "EXEC": tokens.Keyword,
    "EXECUTE": tokens.Keyword,
    "EXISTING": tokens.Keyword,
    "EXISTS": tokens.Keyword,
    "EXPLAIN": tokens.Keyword,
    "EXTERNAL": tokens.Keyword,
    "EXTRACT": tokens.Keyword,
    "FALSE": tokens.Keyword,
    "FETCH": tokens.Keyword,
    "FILE": tokens.Keyword,
    "FINAL": tokens.Keyword,
    "FIRST": tokens.Keyword,
    "FORCE": tokens.Keyword,
    "FOREACH": tokens.Keyword,
    "FOREIGN": tokens.Keyword,
    "FORTRAN": tokens.Keyword,
    "FORWARD": tokens.Keyword,
    "FOUND": tokens.Keyword,
    "FREE": tokens.Keyword,
    "FREEZE": tokens.Keyword,
    "FULL": tokens.Keyword,
    "FUNCTION": tokens.Keyword,
    # 'G': tokens.Keyword,
    "GENERAL": tokens.Keyword,
    "GENERATED": tokens.Keyword,
    "GET": tokens.Keyword,
    "GLOBAL": tokens.Keyword,
    "GO": tokens.Keyword,
    "GOTO": tokens.Keyword,
    "GRANT": tokens.Keyword,
    "GRANTED": tokens.Keyword,
    "GROUPING": tokens.Keyword,
    "HAVING": tokens.Keyword,
    "HIERARCHY": tokens.Keyword,
    "HOLD": tokens.Keyword,
    "HOUR": tokens.Keyword,
    "HOST": tokens.Keyword,
    "IDENTIFIED": tokens.Keyword,
    "IDENTITY": tokens.Keyword,
    "IGNORE": tokens.Keyword,
    "ILIKE": tokens.Keyword,
    "IMMEDIATE": tokens.Keyword,
    "IMMUTABLE": tokens.Keyword,
    "IMPLEMENTATION": tokens.Keyword,
    "IMPLICIT": tokens.Keyword,
    "INCLUDING": tokens.Keyword,
    "INCREMENT": tokens.Keyword,
    "INDEX": tokens.Keyword,
    "INDICATOR": tokens.Keyword,
    "INFIX": tokens.Keyword,
    "INHERITS": tokens.Keyword,
    "INITIAL": tokens.Keyword,
    "INITIALIZE": tokens.Keyword,
    "INITIALLY": tokens.Keyword,
    "INOUT": tokens.Keyword,
    "INPUT": tokens.Keyword,
    "INSENSITIVE": tokens.Keyword,
    "INSTANTIABLE": tokens.Keyword,
    "INSTEAD": tokens.Keyword,
    "INTERSECT": tokens.Keyword,
    "INTO": tokens.Keyword,
    "INVOKER": tokens.Keyword,
    "IS": tokens.Keyword,
    "ISNULL": tokens.Keyword,
    "ISOLATION": tokens.Keyword,
    "ITERATE": tokens.Keyword,
    # 'K': tokens.Keyword,
    "KEY": tokens.Keyword,
    "KEY_MEMBER": tokens.Keyword,
    "KEY_TYPE": tokens.Keyword,
    "LANCOMPILER": tokens.Keyword,
    "LANGUAGE": tokens.Keyword,
    "LARGE": tokens.Keyword,
    "LAST": tokens.Keyword,
    "LATERAL": tokens.Keyword,
    "LEADING": tokens.Keyword,
    "LENGTH": tokens.Keyword,
    "LESS": tokens.Keyword,
    "LEVEL": tokens.Keyword,
    "LIMIT": tokens.Keyword,
    "LISTEN": tokens.Keyword,
    "LOAD": tokens.Keyword,
    "LOCAL": tokens.Keyword,
    "LOCALTIME": tokens.Keyword,
    "LOCALTIMESTAMP": tokens.Keyword,
    "LOCATION": tokens.Keyword,
    "LOCATOR": tokens.Keyword,
    "LOCK": tokens.Keyword,
    "LOWER": tokens.Keyword,
    # 'M': tokens.Keyword,
    "MAP": tokens.Keyword,
    "MATCH": tokens.Keyword,
    "MAXEXTENTS": tokens.Keyword,
    "MAXVALUE": tokens.Keyword,
    "MESSAGE_LENGTH": tokens.Keyword,
    "MESSAGE_OCTET_LENGTH": tokens.Keyword,
    "MESSAGE_TEXT": tokens.Keyword,
    "METHOD": tokens.Keyword,
    "MINUTE": tokens.Keyword,
    "MINUS": tokens.Keyword,
    "MINVALUE": tokens.Keyword,
    "MOD": tokens.Keyword,
    "MODE": tokens.Keyword,
    "MODIFIES": tokens.Keyword,
    "MODIFY": tokens.Keyword,
    "MONTH": tokens.Keyword,
    "MORE": tokens.Keyword,
    "MOVE": tokens.Keyword,
    "MUMPS": tokens.Keyword,
    "NAMES": tokens.Keyword,
    "NATIONAL": tokens.Keyword,
    "NATURAL": tokens.Keyword,
    "NCHAR": tokens.Keyword,
    "NCLOB": tokens.Keyword,
    "NEW": tokens.Keyword,
    "NEXT": tokens.Keyword,
    "NO": tokens.Keyword,
    "NOAUDIT": tokens.Keyword,
    "NOCOMPRESS": tokens.Keyword,
    "NOCREATEDB": tokens.Keyword,
    "NOCREATEUSER": tokens.Keyword,
    "NONE": tokens.Keyword,
    "NOT": tokens.Keyword,
    "NOTFOUND": tokens.Keyword,
    "NOTHING": tokens.Keyword,
    "NOTIFY": tokens.Keyword,
    "NOTNULL": tokens.Keyword,
    "NOWAIT": tokens.Keyword,
    "NULL": tokens.Keyword,
    "NULLABLE": tokens.Keyword,
    "NULLIF": tokens.Keyword,
    "OBJECT": tokens.Keyword,
    "OCTET_LENGTH": tokens.Keyword,
    "OF": tokens.Keyword,
    "OFF": tokens.Keyword,
    "OFFLINE": tokens.Keyword,
    "OFFSET": tokens.Keyword,
    "OIDS": tokens.Keyword,
    "OLD": tokens.Keyword,
    "ONLINE": tokens.Keyword,
    "ONLY": tokens.Keyword,
    "OPEN": tokens.Keyword,
    "OPERATION": tokens.Keyword,
    "OPERATOR": tokens.Keyword,
    "OPTION": tokens.Keyword,
    "OPTIONS": tokens.Keyword,
    "ORDINALITY": tokens.Keyword,
    "OUT": tokens.Keyword,
    "OUTPUT": tokens.Keyword,
    "OVERLAPS": tokens.Keyword,
    "OVERLAY": tokens.Keyword,
    "OVERRIDING": tokens.Keyword,
    "OWNER": tokens.Keyword,
    "QUARTER": tokens.Keyword,
    "PAD": tokens.Keyword,
    "PARAMETER": tokens.Keyword,
    "PARAMETERS": tokens.Keyword,
    "PARAMETER_MODE": tokens.Keyword,
    "PARAMETER_NAME": tokens.Keyword,
    "PARAMETER_ORDINAL_POSITION": tokens.Keyword,
    "PARAMETER_SPECIFIC_CATALOG": tokens.Keyword,
    "PARAMETER_SPECIFIC_NAME": tokens.Keyword,
    "PARAMETER_SPECIFIC_SCHEMA": tokens.Keyword,
    "PARTIAL": tokens.Keyword,
    "PASCAL": tokens.Keyword,
    "PCTFREE": tokens.Keyword,
    "PENDANT": tokens.Keyword,
    "PLACING": tokens.Keyword,
    "PLI": tokens.Keyword,
    "POSITION": tokens.Keyword,
    "POSTFIX": tokens.Keyword,
    "PRECISION": tokens.Keyword,
    "PREFIX": tokens.Keyword,
    "PREORDER": tokens.Keyword,
    "PREPARE": tokens.Keyword,
    "PRESERVE": tokens.Keyword,
    "PRIMARY": tokens.Keyword,
    "PRIOR": tokens.Keyword,
    "PRIVILEGES": tokens.Keyword,
    "PROCEDURAL": tokens.Keyword,
    "PROCEDURE": tokens.Keyword,
    "PUBLIC": tokens.Keyword,
    "RAISE": tokens.Keyword,
    "RAW": tokens.Keyword,
    "READ": tokens.Keyword,
    "READS": tokens.Keyword,
    "RECHECK": tokens.Keyword,
    "RECURSIVE": tokens.Keyword,
    "REF": tokens.Keyword,
    "REFERENCES": tokens.Keyword,
    "REFERENCING": tokens.Keyword,
    "REINDEX": tokens.Keyword,
    "RELATIVE": tokens.Keyword,
    "RENAME": tokens.Keyword,
    "REPEATABLE": tokens.Keyword,
    "RESET": tokens.Keyword,
    "RESOURCE": tokens.Keyword,
    "RESTART": tokens.Keyword,
    "RESTRICT": tokens.Keyword,
    "RESULT": tokens.Keyword,
    "RETURN": tokens.Keyword,
    "RETURNED_LENGTH": tokens.Keyword,
    "RETURNED_OCTET_LENGTH": tokens.Keyword,
    "RETURNED_SQLSTATE": tokens.Keyword,
    "RETURNING": tokens.Keyword,
    "RETURNS": tokens.Keyword,
    "REVOKE": tokens.Keyword,
    "RIGHT": tokens.Keyword,
    "ROLE": tokens.Keyword,
    "ROLLBACK": tokens.Keyword.DML,
    "ROLLUP": tokens.Keyword,
    "ROUTINE": tokens.Keyword,
    "ROUTINE_CATALOG": tokens.Keyword,
    "ROUTINE_NAME": tokens.Keyword,
    "ROUTINE_SCHEMA": tokens.Keyword,
    "ROW": tokens.Keyword,
    "ROWS": tokens.Keyword,
    "ROW_COUNT": tokens.Keyword,
    "RULE": tokens.Keyword,
    "SAVE_POINT": tokens.Keyword,
    "SCALE": tokens.Keyword,
    "SCHEMA": tokens.Keyword,
    "SCHEMA_NAME": tokens.Keyword,
    "SCOPE": tokens.Keyword,
    "SCROLL": tokens.Keyword,
    "SEARCH": tokens.Keyword,
    "SECOND": tokens.Keyword,
    "SECURITY": tokens.Keyword,
    "SELF": tokens.Keyword,
    "SENSITIVE": tokens.Keyword,
    "SEQUENCE": tokens.Keyword,
    "SERIALIZABLE": tokens.Keyword,
    "SERVER_NAME": tokens.Keyword,
    "SESSION": tokens.Keyword,
    "SESSION_USER": tokens.Keyword,
    "SETOF": tokens.Keyword,
    "SETS": tokens.Keyword,
    "SHARE": tokens.Keyword,
    "SHOW": tokens.Keyword,
    "SIMILAR": tokens.Keyword,
    "SIMPLE": tokens.Keyword,
    "SIZE": tokens.Keyword,
    "SOME": tokens.Keyword,
    "SOURCE": tokens.Keyword,
    "SPACE": tokens.Keyword,
    "SPECIFIC": tokens.Keyword,
    "SPECIFICTYPE": tokens.Keyword,
    "SPECIFIC_NAME": tokens.Keyword,
    "SQL": tokens.Keyword,
    "SQLBUF": tokens.Keyword,
    "SQLCODE": tokens.Keyword,
    "SQLERROR": tokens.Keyword,
    "SQLEXCEPTION": tokens.Keyword,
    "SQLSTATE": tokens.Keyword,
    "SQLWARNING": tokens.Keyword,
    "STABLE": tokens.Keyword,
    "START": tokens.Keyword.DML,
    # 'STATE': tokens.Keyword,
    "STATEMENT": tokens.Keyword,
    "STATIC": tokens.Keyword,
    "STATISTICS": tokens.Keyword,
    "STDIN": tokens.Keyword,
    "STDOUT": tokens.Keyword,
    "STORAGE": tokens.Keyword,
    "STRICT": tokens.Keyword,
    "STRUCTURE": tokens.Keyword,
    "STYPE": tokens.Keyword,
    "SUBCLASS_ORIGIN": tokens.Keyword,
    "SUBLIST": tokens.Keyword,
    "SUBSTRING": tokens.Keyword,
    "SUCCESSFUL": tokens.Keyword,
    "SUM": tokens.Keyword,
    "SYMMETRIC": tokens.Keyword,
    "SYNONYM": tokens.Keyword,
    "SYSID": tokens.Keyword,
    "SYSTEM": tokens.Keyword,
    "SYSTEM_USER": tokens.Keyword,
    "TABLE": tokens.Keyword,
    "TABLE_NAME": tokens.Keyword,
    "TEMP": tokens.Keyword,
    "TEMPLATE": tokens.Keyword,
    "TEMPORARY": tokens.Keyword,
    "TERMINATE": tokens.Keyword,
    "THAN": tokens.Keyword,
    "TIMESTAMP": tokens.Keyword,
    "TIMEZONE_HOUR": tokens.Keyword,
    "TIMEZONE_MINUTE": tokens.Keyword,
    "TO": tokens.Keyword,
    "TOAST": tokens.Keyword,
    "TRAILING": tokens.Keyword,
    "TRANSATION": tokens.Keyword,
    "TRANSACTIONS_COMMITTED": tokens.Keyword,
    "TRANSACTIONS_ROLLED_BACK": tokens.Keyword,
    "TRANSATION_ACTIVE": tokens.Keyword,
    "TRANSFORM": tokens.Keyword,
    "TRANSFORMS": tokens.Keyword,
    "TRANSLATE": tokens.Keyword,
    "TRANSLATION": tokens.Keyword,
    "TREAT": tokens.Keyword,
    "TRIGGER": tokens.Keyword,
    "TRIGGER_CATALOG": tokens.Keyword,
    "TRIGGER_NAME": tokens.Keyword,
    "TRIGGER_SCHEMA": tokens.Keyword,
    "TRIM": tokens.Keyword,
    "TRUE": tokens.Keyword,
    "TRUNCATE": tokens.Keyword,
    "TRUSTED": tokens.Keyword,
    "TYPE": tokens.Keyword,
    "UID": tokens.Keyword,
    "UNCOMMITTED": tokens.Keyword,
    "UNDER": tokens.Keyword,
    "UNENCRYPTED": tokens.Keyword,
    "UNION": tokens.Keyword,
    "UNIQUE": tokens.Keyword,
    "UNKNOWN": tokens.Keyword,
    "UNLISTEN": tokens.Keyword,
    "UNNAMED": tokens.Keyword,
    "UNNEST": tokens.Keyword,
    "UNTIL": tokens.Keyword,
    "UPPER": tokens.Keyword,
    "USAGE": tokens.Keyword,
    "USE": tokens.Keyword,
    "USER": tokens.Keyword,
    "USER_DEFINED_TYPE_CATALOG": tokens.Keyword,
    "USER_DEFINED_TYPE_NAME": tokens.Keyword,
    "USER_DEFINED_TYPE_SCHEMA": tokens.Keyword,
    "USING": tokens.Keyword,
    "VACUUM": tokens.Keyword,
    "VALID": tokens.Keyword,
    "VALIDATE": tokens.Keyword,
    "VALIDATOR": tokens.Keyword,
    "VALUES": tokens.Keyword,
    "VARIABLE": tokens.Keyword,
    "VERBOSE": tokens.Keyword,
    "VERSION": tokens.Keyword,
    "VIEW": tokens.Keyword,
    "VOLATILE": tokens.Keyword,
    "WEEK": tokens.Keyword,
    "WHENEVER": tokens.Keyword,
    "WITH": tokens.Keyword.CTE,
    "WITHOUT": tokens.Keyword,
    "WORK": tokens.Keyword,
    "WRITE": tokens.Keyword,
    "YEAR": tokens.Keyword,
    "ZONE": tokens.Keyword,
    # Name.Builtin
    "ARRAY": tokens.Name.Builtin,
    "BIGINT": tokens.Name.Builtin,
    "BINARY": tokens.Name.Builtin,
    "BIT": tokens.Name.Builtin,
    "BLOB": tokens.Name.Builtin,
    "BOOLEAN": tokens.Name.Builtin,
    "CHAR": tokens.Name.Builtin,
    "CHARACTER": tokens.Name.Builtin,
    "DATE": tokens.Name.Builtin,
    "DEC": tokens.Name.Builtin,
    "DECIMAL": tokens.Name.Builtin,
    "FILE_TYPE": tokens.Name.Builtin,
    "FLOAT": tokens.Name.Builtin,
    "INT": tokens.Name.Builtin,
    "INT8": tokens.Name.Builtin,
    "INTEGER": tokens.Name.Builtin,
    "INTERVAL": tokens.Name.Builtin,
    "LONG": tokens.Name.Builtin,
    "NATURALN": tokens.Name.Builtin,
    "NVARCHAR": tokens.Name.Builtin,
    "NUMBER": tokens.Name.Builtin,
    "NUMERIC": tokens.Name.Builtin,
    "PLS_INTEGER": tokens.Name.Builtin,
    "POSITIVE": tokens.Name.Builtin,
    "POSITIVEN": tokens.Name.Builtin,
    "REAL": tokens.Name.Builtin,
    "ROWID": tokens.Name.Builtin,
    "ROWLABEL": tokens.Name.Builtin,
    "ROWNUM": tokens.Name.Builtin,
    "SERIAL": tokens.Name.Builtin,
    "SERIAL8": tokens.Name.Builtin,
    "SIGNED": tokens.Name.Builtin,
    "SIGNTYPE": tokens.Name.Builtin,
    "SIMPLE_DOUBLE": tokens.Name.Builtin,
    "SIMPLE_FLOAT": tokens.Name.Builtin,
    "SIMPLE_INTEGER": tokens.Name.Builtin,
    "SMALLINT": tokens.Name.Builtin,
    "SYS_REFCURSOR": tokens.Name.Builtin,
    "SYSDATE": tokens.Name,
    "TEXT": tokens.Name.Builtin,
    "TINYINT": tokens.Name.Builtin,
    "UNSIGNED": tokens.Name.Builtin,
    "UROWID": tokens.Name.Builtin,
    "UTL_FILE": tokens.Name.Builtin,
    "VARCHAR": tokens.Name.Builtin,
    "VARCHAR2": tokens.Name.Builtin,
    "VARYING": tokens.Name.Builtin,
}

KEYWORDS_COMMON = {
    "SELECT": tokens.Keyword.DML,
    "INSERT": tokens.Keyword.DML,
    "DELETE": tokens.Keyword.DML,
    "UPDATE": tokens.Keyword.DML,
    "UPSERT": tokens.Keyword.DML,
    "REPLACE": tokens.Keyword.DML,
    "MERGE": tokens.Keyword.DML,
    "DROP": tokens.Keyword.DDL,
    "CREATE": tokens.Keyword.DDL,
    "ALTER": tokens.Keyword.DDL,
    "WHERE": tokens.Keyword,
    "FROM": tokens.Keyword,
    "INNER": tokens.Keyword,
    "JOIN": tokens.Keyword,
    "STRAIGHT_JOIN": tokens.Keyword,
    "AND": tokens.Keyword,
    "OR": tokens.Keyword,
    "LIKE": tokens.Keyword,
    "ON": tokens.Keyword,
    "IN": tokens.Keyword,
    "SET": tokens.Keyword,
    "BY": tokens.Keyword,
    "GROUP": tokens.Keyword,
    "ORDER": tokens.Keyword,
    "LEFT": tokens.Keyword,
    "OUTER": tokens.Keyword,
    "FULL": tokens.Keyword,
    "IF": tokens.Keyword,
    "END": tokens.Keyword,
    "THEN": tokens.Keyword,
    "LOOP": tokens.Keyword,
    "AS": tokens.Keyword,
    "ELSE": tokens.Keyword,
    "FOR": tokens.Keyword,
    "WHILE": tokens.Keyword,
    "CASE": tokens.Keyword,
    "WHEN": tokens.Keyword,
    "MIN": tokens.Keyword,
    "MAX": tokens.Keyword,
    "DISTINCT": tokens.Keyword,
}

KEYWORDS_ORACLE = {
    "ARCHIVE": tokens.Keyword,
    "ARCHIVELOG": tokens.Keyword,
    "BACKUP": tokens.Keyword,
    "BECOME": tokens.Keyword,
    "BLOCK": tokens.Keyword,
    "BODY": tokens.Keyword,
    "CANCEL": tokens.Keyword,
    "CHANGE": tokens.Keyword,
    "COMPILE": tokens.Keyword,
    "CONTENTS": tokens.Keyword,
    "CONTROLFILE": tokens.Keyword,
    "DATAFILE": tokens.Keyword,
    "DBA": tokens.Keyword,
    "DISMOUNT": tokens.Keyword,
    "DOUBLE": tokens.Keyword,
    "DUMP": tokens.Keyword,
    "ELSIF": tokens.Keyword,
    "EVENTS": tokens.Keyword,
    "EXCEPTIONS": tokens.Keyword,
    "EXPLAIN": tokens.Keyword,
    "EXTENT": tokens.Keyword,
    "EXTERNALLY": tokens.Keyword,
    "FLUSH": tokens.Keyword,
    "FREELIST": tokens.Keyword,
    "FREELISTS": tokens.Keyword,
    # groups seems too common as table name
    # 'GROUPS': tokens.Keyword,
    "INDICATOR": tokens.Keyword,
    "INITRANS": tokens.Keyword,
    "INSTANCE": tokens.Keyword,
    "LAYER": tokens.Keyword,
    "LINK": tokens.Keyword,
    "LISTS": tokens.Keyword,
    "LOGFILE": tokens.Keyword,
    "MANAGE": tokens.Keyword,
    "MANUAL": tokens.Keyword,
    "MAXDATAFILES": tokens.Keyword,
    "MAXINSTANCES": tokens.Keyword,
    "MAXLOGFILES": tokens.Keyword,
    "MAXLOGHISTORY": tokens.Keyword,
    "MAXLOGMEMBERS": tokens.Keyword,
    "MAXTRANS": tokens.Keyword,
    "MINEXTENTS": tokens.Keyword,
    "MODULE": tokens.Keyword,
    "MOUNT": tokens.Keyword,
    "NOARCHIVELOG": tokens.Keyword,
    "NOCACHE": tokens.Keyword,
    "NOCYCLE": tokens.Keyword,
    "NOMAXVALUE": tokens.Keyword,
    "NOMINVALUE": tokens.Keyword,
    "NOORDER": tokens.Keyword,
    "NORESETLOGS": tokens.Keyword,
    "NORMAL": tokens.Keyword,
    "NOSORT": tokens.Keyword,
    "OPTIMAL": tokens.Keyword,
    "OWN": tokens.Keyword,
    "PACKAGE": tokens.Keyword,
    "PARALLEL": tokens.Keyword,
    "PCTINCREASE": tokens.Keyword,
    "PCTUSED": tokens.Keyword,
    "PLAN": tokens.Keyword,
    "PRIVATE": tokens.Keyword,
    "PROFILE": tokens.Keyword,
    "QUOTA": tokens.Keyword,
    "RECOVER": tokens.Keyword,
    "RESETLOGS": tokens.Keyword,
    "RESTRICTED": tokens.Keyword,
    "REUSE": tokens.Keyword,
    "ROLES": tokens.Keyword,
    "SAVEPOINT": tokens.Keyword,
    "SCN": tokens.Keyword,
    "SECTION": tokens.Keyword,
    "SEGMENT": tokens.Keyword,
    "SHARED": tokens.Keyword,
    "SNAPSHOT": tokens.Keyword,
    "SORT": tokens.Keyword,
    "STATEMENT_ID": tokens.Keyword,
    "STOP": tokens.Keyword,
    "SWITCH": tokens.Keyword,
    "TABLES": tokens.Keyword,
    "TABLESPACE": tokens.Keyword,
    "THREAD": tokens.Keyword,
    "TIME": tokens.Keyword,
    "TRACING": tokens.Keyword,
    "TRANSACTION": tokens.Keyword,
    "TRIGGERS": tokens.Keyword,
    "UNLIMITED": tokens.Keyword,
    "UNLOCK": tokens.Keyword,
}

# PostgreSQL Syntax
KEYWORDS_PLPGSQL = {
    "CONFLICT": tokens.Keyword,
    "WINDOW": tokens.Keyword,
    "PARTITION": tokens.Keyword,
    "OVER": tokens.Keyword,
    "PERFORM": tokens.Keyword,
    "NOTICE": tokens.Keyword,
    "PLPGSQL": tokens.Keyword,
    "INHERIT": tokens.Keyword,
    "INDEXES": tokens.Keyword,
    "ON_ERROR_STOP": tokens.Keyword,
    "BYTEA": tokens.Keyword,
    "BIGSERIAL": tokens.Keyword,
    "BIT VARYING": tokens.Keyword,
    "BOX": tokens.Keyword,
    "CHARACTER": tokens.Keyword,
    "CHARACTER VARYING": tokens.Keyword,
    "CIDR": tokens.Keyword,
    "CIRCLE": tokens.Keyword,
    "DOUBLE PRECISION": tokens.Keyword,
    "INET": tokens.Keyword,
    "JSON": tokens.Keyword,
    "JSONB": tokens.Keyword,
    "LINE": tokens.Keyword,
    "LSEG": tokens.Keyword,
    "MACADDR": tokens.Keyword,
    "MONEY": tokens.Keyword,
    "PATH": tokens.Keyword,
    "PG_LSN": tokens.Keyword,
    "POINT": tokens.Keyword,
    "POLYGON": tokens.Keyword,
    "SMALLSERIAL": tokens.Keyword,
    "TSQUERY": tokens.Keyword,
    "TSVECTOR": tokens.Keyword,
    "TXID_SNAPSHOT": tokens.Keyword,
    "UUID": tokens.Keyword,
    "XML": tokens.Keyword,
    "FOR": tokens.Keyword,
    "IN": tokens.Keyword,
    "LOOP": tokens.Keyword,
}

# Hive Syntax
KEYWORDS_HQL = {
    "EXPLODE": tokens.Keyword,
    "DIRECTORY": tokens.Keyword,
    "DISTRIBUTE": tokens.Keyword,
    "INCLUDE": tokens.Keyword,
    "LOCATE": tokens.Keyword,
    "OVERWRITE": tokens.Keyword,
    "POSEXPLODE": tokens.Keyword,
    "ARRAY_CONTAINS": tokens.Keyword,
    "CMP": tokens.Keyword,
    "COLLECT_LIST": tokens.Keyword,
    "CONCAT": tokens.Keyword,
    "CONDITION": tokens.Keyword,
    "DATE_ADD": tokens.Keyword,
    "DATE_SUB": tokens.Keyword,
    "DECODE": tokens.Keyword,
    "DBMS_OUTPUT": tokens.Keyword,
    "ELEMENTS": tokens.Keyword,
    "EXCHANGE": tokens.Keyword,
    "EXTENDED": tokens.Keyword,
    "FLOOR": tokens.Keyword,
    "FOLLOWING": tokens.Keyword,
    "FROM_UNIXTIME": tokens.Keyword,
    "FTP": tokens.Keyword,
    "HOUR": tokens.Keyword,
    "INLINE": tokens.Keyword,
    "INSTR": tokens.Keyword,
    "LEN": tokens.Keyword,
    "MAP": tokens.Name.Builtin,
    "MAXELEMENT": tokens.Keyword,
    "MAXINDEX": tokens.Keyword,
    "MAX_PART_DATE": tokens.Keyword,
    "MAX_PART_INT": tokens.Keyword,
    "MAX_PART_STRING": tokens.Keyword,
    "MINELEMENT": tokens.Keyword,
    "MININDEX": tokens.Keyword,
    "MIN_PART_DATE": tokens.Keyword,
    "MIN_PART_INT": tokens.Keyword,
    "MIN_PART_STRING": tokens.Keyword,
    "NOW": tokens.Keyword,
    "NVL": tokens.Keyword,
    "NVL2": tokens.Keyword,
    "PARSE_URL_TUPLE": tokens.Keyword,
    "PART_LOC": tokens.Keyword,
    "PART_COUNT": tokens.Keyword,
    "PART_COUNT_BY": tokens.Keyword,
    "PRINT": tokens.Keyword,
    "PUT_LINE": tokens.Keyword,
    "RANGE": tokens.Keyword,
    "REDUCE": tokens.Keyword,
    "REGEXP_REPLACE": tokens.Keyword,
    "RESIGNAL": tokens.Keyword,
    "RTRIM": tokens.Keyword,
    "SIGN": tokens.Keyword,
    "SIGNAL": tokens.Keyword,
    "SIN": tokens.Keyword,
    "SPLIT": tokens.Keyword,
    "SQRT": tokens.Keyword,
    "STACK": tokens.Keyword,
    "STR": tokens.Keyword,
    "STRING": tokens.Name.Builtin,
    "STRUCT": tokens.Name.Builtin,
    "SUBSTR": tokens.Keyword,
    "SUMMARY": tokens.Keyword,
    "TBLPROPERTIES": tokens.Keyword,
    "TIMESTAMP": tokens.Name.Builtin,
    "TIMESTAMP_ISO": tokens.Keyword,
    "TO_CHAR": tokens.Keyword,
    "TO_DATE": tokens.Keyword,
    "TO_TIMESTAMP": tokens.Keyword,
    "TRUNC": tokens.Keyword,
    "UNBOUNDED": tokens.Keyword,
    "UNIQUEJOIN": tokens.Keyword,
    "UNIX_TIMESTAMP": tokens.Keyword,
    "UTC_TIMESTAMP": tokens.Keyword,
    "VIEWS": tokens.Keyword,
    "EXIT": tokens.Keyword,
    "BREAK": tokens.Keyword,
    "LEAVE": tokens.Keyword,
}


KEYWORDS_MSACCESS = {
    "DISTINCTROW": tokens.Keyword,
}
