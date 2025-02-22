import importlib
import types


def import_extractor_module(
    lang_code: str, module_name: str
) -> types.ModuleType:
    default_module_name = f"wiktextract.extractor.en.{module_name}"
    try:
        full_module_name = f"wiktextract.extractor.{lang_code}.{module_name}"
        module_spec = importlib.util.find_spec(full_module_name)
        if module_spec is None:
            full_module_name = default_module_name
    except ModuleNotFoundError:
        full_module_name = default_module_name

    return importlib.import_module(full_module_name)
