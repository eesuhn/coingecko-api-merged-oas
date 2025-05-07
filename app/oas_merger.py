import requests

from ._constants import (
    OAS_BASE_URL,
    COINGECKO_PRO,
    COINGECKO_ONCHAIN_PRO
)
from .utils import (
    load_json,
    save_json,
    print_success,
    get_package_root,
    print_info
)


class OASMerger:
    def run(self) -> None:
        self.coingecko_pro = self.get_oas_json(
            path=COINGECKO_PRO
        )
        self.coingecko_onchain_pro = self.get_oas_json(
            path=COINGECKO_ONCHAIN_PRO
        )
        self.merge_oas()

    def get_oas_json(
        self,
        path: str
    ) -> dict:
        url = f"{OAS_BASE_URL}/{path}.json"
        response = requests.get(
            url=url,
            timeout=10
        )
        if response.status_code != 200:
            raise ValueError(response.text)
        print_success(f"Fetched {path}")
        return response.json()

    def merge_oas(self) -> None:
        oas = load_json(
            filename="docs/default-oas"
        )
        oas["paths"] = self.merge_paths()
        oas["components"]["schemas"] = self.merge_schemas()
        save_json(
            data=oas,
            filename="docs/coingecko"
        )
        print_success(f"Merged OAS at {get_package_root() / 'docs/coingecko.json'}")

    def merge_paths(self) -> dict:
        paths = {}
        pro_paths_count = 0
        onchain_paths_count = 0
        for path, item in self.coingecko_pro.get("paths", {}).items():
            if path in paths:
                raise ValueError(f"Duplicate path: {path}")
            paths[path] = item
            pro_paths_count += 1
        for path, item in self.coingecko_onchain_pro.get("paths", {}).items():
            new_path = "/onchain" + path if not path.startswith("/onchain") else path
            if new_path in paths:
                raise ValueError(f"Duplicate path: {new_path}")
            paths[new_path] = item
            onchain_paths_count += 1
        self.check_operation_id(paths)
        paths_count = pro_paths_count + onchain_paths_count
        print_info(f"Merged {paths_count} OAS paths: {onchain_paths_count} from /onchain")
        return paths

    def check_operation_id(
        self,
        paths: dict
    ) -> None:
        operation_ids: dict = {}
        for path, item in paths.items():
            for _, v in item.items():
                if isinstance(v, dict) and "operationId" in v:
                    operation_id = v["operationId"]
                    if operation_id in operation_ids:
                        raise ValueError(f"Duplicate operationId: {operation_id}")
                    operation_ids[operation_id] = path

    def merge_schemas(self) -> dict:
        schemas = {}
        pro_schemas_count = 0
        onchain_schemas_count = 0
        for key, schema in self.coingecko_pro.get("components", {}).get("schemas", {}).items():
            if key in schemas:
                raise ValueError(f"Duplicate schema: {key}")
            schemas[key] = schema
            pro_schemas_count += 1
        for key, schema in self.coingecko_onchain_pro.get("components", {}).get("schemas", {}).items():
            if key in schemas:
                raise ValueError(f"Duplicate schema: {key}")
            schemas[key] = schema
            onchain_schemas_count += 1
        schemas_count = pro_schemas_count + onchain_schemas_count
        print_info(f"Merged {schemas_count} OAS schemas: {onchain_schemas_count} from /onchain")
        return schemas
